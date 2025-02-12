The authors introduced a **Cherry Chevre: A Fine-Grained Dataset for Goat Detection in Natural Environments** dataset for goat detection that contains 6160 annotated images captured under varying environmental conditions. The dataset is intended for developing machine learning algorithms for goat detection, with applications in precision agriculture, animal welfare, behaviour analysis, and animal husbandry. The annotations were performed by expert in computer vision, ensuring high accuracy and consistency.

## Motivation

Goats, widely kept as livestock globally, are recognized for their adaptability, high productivity, and the quality of their milk and meat. Nevertheless, researchers encounter the challenge of efficiently detecting and monitoring goat herds to analyze their behavior. Visual observation, a time-consuming and error-prone method, poses difficulties in acquiring detailed data on the precise movements and behaviors of goats. An alternative approach involves utilizing GPS, but this method requires handling the animals and may be inaccurate, particularly in isolated locations, especially when monitoring at a pasture scale.

Automated methods employing computer vision techniques offer a promising solution to overcome challenges in behavior analysis. However, the successful development of these techniques relies heavily on the availability of high-quality datasets for training and evaluation. Despite the presence of livestock detection datasets, there remains a notable scarcity of comprehensive, high-quality datasets specifically designed for goat detection. Furthermore, the accuracy of detection is intricately linked to the quality of the dataset.

To address this gap, the authors present the inaugural dataset for goat detection, comprising 6160 annotated images of goats captured under diverse environmental conditions. These images were collected through field surveys, and each image was meticulously annotated with bounding boxes delineating the goat's body. The bounding boxes adhere at the pixel level around the body, accounting for factors such as feet on leaves and fur that may create blur. The annotations were executed by a proficient expert in the field of computer vision, ensuring a high degree of accuracy and consistency. The dataset encompasses images depicting goats in various poses and orientations, including standing, grazing, and lying down, captured under varying lighting conditions, ranging from bright sunlight to low light.

## Data Acquisition

* **Cross-call.** The ***crosscall*** Trecker X2, a robust smartphone, served as the imaging tool for capturing a total of 297 images at different dates and times, providing a diverse range of lighting and environmental conditions. This device is equipped with advanced sensors, ensuring the capture of high-quality images. The Trecker X2's rear camera boasts a 12-megapixel sensor with an aperture of f/2.0, enabling the capture of clear and sharp images even in low-light conditions. Similar to contemporary smartphones, it features an auto-focus system to guarantee that images are consistently in focus. The image collection took place at the INRAE-Duclos facility in Guadeloupe, French West Indies, with some shots near Albiez-Montrond and others near Tesq and Montpeyroux in France during 2020. The dataset encompasses a variety of subjects, including white sheep, goats, and predominantly Creole sheep, which bear a striking resemblance to European goats in appearance.

* **Phantom3.** Creole goats, engaging in grazing activities across two distinct pastures (G1 + G2), were documented using a ***phantom3*** UAV drone equipped with a 12-megapixel camera sensor. The camera, featuring a 94-degree field of view lens for expansive shots, captured images at a maximum resolution of 4000 × 3000 px. The observational study spanned four consecutive days in April 2017 at the INRA-PTEA farm (16° 2 N; 61° 2 W), with a total of 47 images re-annotated to include young goats (kids). To accommodate the small size of the animals and the large image dimensions, each original image was subdivided into smaller segments, resulting in 696 images, each with dimensions of 1000 × 750 px.

| Source | Date       | Images |
|--------|------------|--------|
| G1     | 10/04/2017 | 299    |
| G2     | 10/04/2017 | 281    |
| G1     | 11/04/2017 | 35     |
| G2     | 11/04/2017 | 46     |
| G1     | 12/04/2017 | 35     |
| Videos | 13/04/2017 | 150    |

<span style="font-size: smaller; font-style: italic;">Number of annotated images by date for the Phantom3.</span>

* **Time-lapse camera.** The researchers utilized construction ***timelapse camera***, specifically the TLC2000 pro model from the year 2018 manufactured by Brinno, a brand previously employed in various studies. These cameras capture images at 1.3 megapixels with a resolution of 1280 × 720 px, utilizing jpeg compression. In the initial phase of the study, distinct experimental plots were established to investigate the detection and tracking of goats and sheep. The first subset comprised seven indoor-raised Creole sheep with identical reddish coats. The second dataset featured a single Creole sheep with a brown coat, while the third included nine goats in close proximity to the camera, six of them sporting dark coats and the remainder having red coats. Additionally, a few distant goats were annotated in the dataset. Building on prior research, the authors expanded their dataset by collecting additional data in natural environments encompassing various lighting conditions. The established framework from earlier studies underwent refinement and testing as the researchers monitored two goat herds in farm-like conditions. One ***timelapse camera*** was deployed to observe an area approximately 20 × 20 meters, and multiple cameras were strategically combined to monitor the entirety of the pasture.

| Date | Study  | Images |
|------|--------|--------|
| 2018 | 19     | 140    |
| 2020 | 20,21  | 1446   |
| 2022 | 22     | 784    |

<span style="font-size: smaller; font-style: italic;">Number of annotated images by date for the TLC2000 device.</span>


* **Tracking series.** A CCTV camera (ENEO - IPD-75M2713M5A) boasting a resolution of 2592 × 1944 px was employed to record 17 videos capturing goats grazing in a pasture throughout 2022 over five distinct days. The purpose behind this recording was the development of a ***tracking*** algorithm. Each video was subsampled to yield 98 images, comprising 50 with non-overlapping goats and 50 featuring a minimum of two goats overlapping. These video sessions occurred at two locations within the INRAE-PTEA facility in Guadeloupe, French West Indies. In early 2023, an additional set of six videos was created over three separate days at the experimental plot in Duclos. These videos featured male goats exhibiting varied coat colors, including dark, white, russet, and dark-russet. Each goat was equipped with a collar, distinguished by red, yellow, orange, and blue colors, respectively, to facilitate the attachment of an accelerometer. Concurrently, eight more videos were recorded at Gardel in early 2023, spanning four different days.

| Date       | Location | Images |
|------------|----------|--------|
| 12/04/2022 | Duclos   | 98     |
| 22/04/2022 | Duclos   | 687    |
| 26/04/2022 | Duclos   | 197    |
| 17/02/2023 | Duclos   | 136    |
| 23/02/2023 | Duclos   | 280    |
| 24/02/2023 | Duclos   | 97     |
| 02/05/2022 | Gardel   | 196    |
| 16/06/2022 | Gardel   | 489    |
| 14/03/2023 | Gardel   | 146    |
| 16/03/2023 | Gardel   | 33     |
| 17/03/2023 | Gardel   | 25     |
| 24/03/2023 | Gardel   | 25     |

<span style="font-size: smaller; font-style: italic;">Dates, location and number of annotated images, using the ENEO camera.</span>

* **External.** This subset amalgamates images from two distinct sites. The first site, named Mosar, is situated at the INRAE UMR 791 in Grignon, France. Within this subset, European goats housed indoors are featured, showcasing two pens each accommodating eight animals. The camera and feeding tray setup primarily captures the goats from behind, with a sub-sampling of four 30-minute videos. The second collaborator is situated at the Experimental Unit FERLUS, presenting a limited collection of ground-level images depicting European goats in an outdoor pasture. The image sizes for the first and second subsets are 1280 × 720 px and 4032 × 3024 px, respectively.

| Date       | Location | Images |
|------------|----------|--------|
| 23/03/2022 | Mosar-p1 | 151    |
| 23/03/2022 | Mosar-p2 | 45     |
| 23/03/2022 | Mosar-p3 | 45     |
| 23/03/2022 | Mosar-p4 | 44     |
| 10/03/2016 | Ferlus   | 14     |

<span style="font-size: smaller; font-style: italic;">Date, location and number of annotated images for external sources.</span>

