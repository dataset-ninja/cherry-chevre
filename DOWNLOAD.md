Dataset **Cherry Chevre** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://www.dropbox.com/scl/fi/ztfpsx4til97j2lpl2pvo/cherry-chevre-DatasetNinja.tar?rlkey=jv6yjpeogvnd77v7d556k8422&dl=1)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='Cherry Chevre', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://entrepot.recherche.data.gouv.fr/dataset.xhtml?persistentId=doi:10.57745/QEZBNA#).