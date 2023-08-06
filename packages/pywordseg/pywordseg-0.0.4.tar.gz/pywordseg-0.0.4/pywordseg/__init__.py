import os
if not os.path.isdir(os.path.join(os.path.abspath(os.path.join(__file__ ,"..")), "CharEmb")):
    from .download import save_unzip
    print("first use, download CharEmb.")
    filename = "CharEmb.zip"
    url = "https://www.dropbox.com/s/t0o52grcrd3zixd/CharEmb.zip?dl=1"
    save_unzip(url, filename)
if not os.path.isdir(os.path.join(os.path.abspath(os.path.join(__file__ ,"..")), "models")):
    from .download import save_unzip
    print("first use, download models.")
    filename = "models.zip"
    url = "https://www.dropbox.com/s/83se2r05501ysyr/models.zip?dl=1"
    save_unzip(url, filename)
if not os.path.isdir(os.path.join(os.path.abspath(os.path.join(__file__ ,"..")), "ELMoForManyLangs")):
    from .download import save_unzip
    print("first use, download ELMoForManyLangs.")
    filename = "ELMoForManyLangs.zip"
    url = "https://www.dropbox.com/s/eiya6ztmjopprsm/ELMoForManyLangs.zip?dl=1"
    save_unzip(url, filename)
from .pywordseg import Wordseg
