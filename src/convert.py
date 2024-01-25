import ast
import csv
import os
import shutil
from collections import defaultdict
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name, get_file_name_with_ext
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/CherryChevre/dataverse_files/data"
    train_split_path = "/home/alex/DATASETS/TODO/CherryChevre/dataverse_files/train.csv"
    val_split_path = "/home/alex/DATASETS/TODO/CherryChevre/dataverse_files/valid.csv"
    test_split_path = "/home/alex/DATASETS/TODO/CherryChevre/dataverse_files/test.csv"
    tracking_path = "/home/alex/DATASETS/TODO/CherryChevre/dataverse_files/data/Tracking"
    batch_size = 30
    ann_ext = ".csv"

    def create_ann(image_path):
        labels = []
        tags = []

        subfolder_value = image_path.split("/")[-2]
        subfolder = sly.Tag(subfolder_meta, value=subfolder_value)
        tags.append(subfolder)

        method_value = image_path.split("/")[-3]
        if method_value not in ["Crosscall", "External", "Phantom3", "TimelapsCamera"]:
            method = sly.Tag(tracking_meta)
            tags.append(method)
            year_value = image_path.split("/")[-4]
            year_meta = folder_to_year.get(year_value)
            year = sly.Tag(year_meta)
            tags.append(year)
        else:
            method_meta = folder_to_meta.get(method_value)
            method = sly.Tag(method_meta)
            tags.append(method)

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        ann_data = path_to_anns.get(image_path)
        for curr_ann_data_str in ann_data:
            curr_ann_data = ast.literal_eval(curr_ann_data_str)

            left = curr_ann_data["x"]
            top = curr_ann_data["y"]
            right = left + curr_ann_data["width"]
            bottom = top + curr_ann_data["height"]
            if top < 0 or left < 0:
                continue
            rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
            label = sly.Label(rect, obj_class)
            labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    obj_class = sly.ObjClass("animal", sly.Rectangle)

    crosscall_meta = sly.TagMeta("crosscall", sly.TagValueType.NONE)
    external_meta = sly.TagMeta("external", sly.TagValueType.NONE)
    phantom3_meta = sly.TagMeta("phantom3", sly.TagValueType.NONE)
    timelaps_meta = sly.TagMeta("timelaps camera", sly.TagValueType.NONE)
    tracking_meta = sly.TagMeta("tracking", sly.TagValueType.NONE)
    subfolder_meta = sly.TagMeta("subfolder", sly.TagValueType.ANY_STRING)
    year2023_meta = sly.TagMeta("2023", sly.TagValueType.NONE)
    year2022_meta = sly.TagMeta("2022", sly.TagValueType.NONE)

    folder_to_meta = {
        "Crosscall": crosscall_meta,
        "External": external_meta,
        "Phantom3": phantom3_meta,
        "TimelapsCamera": timelaps_meta,
        "Tracking": tracking_meta,
    }

    folder_to_year = {"2023": year2023_meta, "2022": year2022_meta}

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=[obj_class],
        tag_metas=[
            crosscall_meta,
            external_meta,
            phantom3_meta,
            timelaps_meta,
            tracking_meta,
            subfolder_meta,
            year2023_meta,
            year2022_meta,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())

    path_to_anns = defaultdict(list)

    for curr_folder in os.listdir(dataset_path):
        if curr_folder == "Tracking":
            continue
        curr_path = os.path.join(dataset_path, curr_folder)
        for curr_subitem in os.listdir(curr_path):
            curr_subitem_path = os.path.join(curr_path, curr_subitem)
            if file_exists(curr_subitem_path):
                with open(curr_subitem_path, "r") as file:
                    csvreader = csv.reader(file)
                    for idx, row in enumerate(csvreader):
                        if idx == 0:
                            continue
                        path_to_anns[
                            curr_path + "/" + get_file_name(curr_subitem) + "/" + row[0]
                        ].append(row[5])

    for curr_folder in os.listdir(tracking_path):
        curr_path = os.path.join(tracking_path, curr_folder)
        for temp_folder in os.listdir(curr_path):
            temp_path = os.path.join(curr_path, temp_folder)
            for curr_subitem in os.listdir(temp_path):
                curr_subitem_path = os.path.join(temp_path, curr_subitem)
                if file_exists(curr_subitem_path):
                    with open(curr_subitem_path, "r") as file:
                        csvreader = csv.reader(file)
                        for idx, row in enumerate(csvreader):
                            if idx == 0:
                                continue
                            path_to_anns[
                                temp_path + "/" + get_file_name(curr_subitem) + "/" + row[0]
                            ].append(row[5])

    train_pathes = []
    with open(train_split_path, "r") as file:
        csvreader = csv.reader(file)
        for idx, row in enumerate(csvreader):
            if idx == 0:
                continue
            train_pathes.append(os.path.join(dataset_path, row[1]))

    val_pathes = []
    with open(val_split_path, "r") as file:
        csvreader = csv.reader(file)
        for idx, row in enumerate(csvreader):
            if idx == 0:
                continue
            val_pathes.append(os.path.join(dataset_path, row[1]))

    test_pathes = []
    with open(test_split_path, "r") as file:
        csvreader = csv.reader(file)
        for idx, row in enumerate(csvreader):
            if idx == 0:
                continue
            test_pathes.append(os.path.join(dataset_path, row[1]))

    ds_name_to_data = {"train": train_pathes, "val": val_pathes, "test": test_pathes}

    for ds_name, images_pathes in ds_name_to_data.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

        for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            images_names_batch = [
                im_path.split("/")[-2] + "_" + get_file_name_with_ext(im_path)
                for im_path in img_pathes_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
