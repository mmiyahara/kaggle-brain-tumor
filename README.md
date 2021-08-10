# [kaggle-brain-tumor](https://www.kaggle.com/c/rsna-miccai-brain-tumor-radiogenomic-classification)

![schedule](assets/diagram.png)

## Overview

- 脳の悪性腫瘍の話
- MGMT promoter methylation があれば化学療法が効きやすい
- MGMT promoter methylation の判定には手術が必要で大変

  → 機械学習で MRI 画像から MGMT promoter methylation の有無を判定する

## Diagram

- Init

```
docker pull minlag/mermaid-cli
```

- Edit

```
vi assets/diagram.mmd
```

- Build

```
rm -f assets/diagram.png
docker run -it -v $(pwd)/assets:/data minlag/mermaid-cli -i /data/diagram.mmd -o /data/diagram.png
```

## Docs

| Title                                                                                                                               | Status  | Comment                                                              |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------- |
| [Getting started with Google Colab](https://www.kaggle.com/reubenschmidt/getting-started-in-rsna-miccai-with-google-colab/comments) | READ    | Colab で分析するチュートリアル、データサイズ上限により無料版では不可 |
| [EDA for starter](https://www.kaggle.com/chumajin/brain-tumor-eda-for-starter-version)                                              | READ    | 画像の表示方法と `SliceLocation` について参考になった                |
| [EDA+3D-Baseline](https://www.kaggle.com/dschettler8845/eda-3d-baseline-rsna-glioma-radiogenomics)                                  | Not yet |                                                                      |
| [Create 3D NPZ & TFRecords](https://www.kaggle.com/dschettler8845/create-3d-npz-tfrecords-rsna-radiogenomics)                       | Not yet |                                                                      |
| [Brain Tumor - EDA](https://www.kaggle.com/tanlikesmath/brain-tumor-radiogenomic-classification-eda?scriptVersionId=68158398)       | Not yet |                                                                      |

## Diary

### 2021/08/08

- 概要読んでローカルにダウンロードしようとしたけどデータセット大きすぎる & 画像データなのでローカルで捌ききれないと判断
  - Google Colab で試したが、無料版のディスク容量ではデータセットを保存できない
  - Kaggle Notebook で
- 提出するファイルは以下（`submission.csv`）

  | BraTS21ID | MGMT_value |
  | --------- | ---------- |
  | 1         | 0          |
  | 2         | 1          |
  | 3         | 0          |
  | ...       | ...        |

  - `BraTS21ID`: 患者 ID
  - `MGMT_value` - `0`: MGMT プロモーターがメチル化されていない - `1`: MGMT プロモーターがメチル化されている

### 2021/08/09

- [2021/08/09 Brain Tumor - Count # of images](https://www.kaggle.com/mstkmyhr/2021-08-09-brain-tumor-count-of-images)

  - 患者 id ごとに 4 種類の MRI 画像が含まれている
  - MRI 画像の数は患者ごとにばらばら

  ![count](assets/20210809_count.png)

  - 各 MRI 画像のファイル数の分布。

  ![histogram](assets/20210809_histogram.png)

- [EDA for starter](https://www.kaggle.com/chumajin/brain-tumor-eda-for-starter-version) を読んだ

  - DICOM = MRI 含む医療用画像の保存形式
  - [pydicom](https://pydicom.github.io/pydicom/stable/old/getting_started.html) = DICOM 形式のファイルを扱う Python パッケージ
  - 画像の表示方法がわかった（[2021/08/09 Brain Tumor - See MRI Images](https://www.kaggle.com/mstkmyhr/2021-08-09-brain-tumor-see-mri-images)で試した）
  - ファイル番号 != 時系列 な場合がある。`.dcm` ファイルの `SliceLocation` でソートすると時系列に並ぶ
    （断面図を上から撮影していくが、上の断面図から下の断面図の順に並べることができる）

- [2021/08/09 Brain Tumor - See MRI Images](https://www.kaggle.com/mstkmyhr/2021-08-09-brain-tumor-see-mri-images)

  - メチル化患者の FLAIR で右上が光る傾向がある？と思ったが、
    False(id = 803) でも右上が光っているのでそうでもない

- [2021/08/09 Brain Tumor - Attributes](https://www.kaggle.com/mstkmyhr/2021-08-09-brain-tumor-attributes)

  - 断面図を上から下の順に並べるには、たしかに `SliceLocation` で良さそう（`ImagePositionPatient` の y 軸でも同じ）
    ```
      AccessionNumber:00000
      ...
      ImageOrientationPatient:[1, -0, 0, -0, -0, -1]
    - ImagePositionPatient:[-125.094, 30.9865, 127.74]
    ?                                    ^
    + ImagePositionPatient:[-125.094, 30.3865, 127.74]
    ?                                    ^
      ImageType:['DERIVED', 'SECONDARY']
      ...
    - InStackPositionNumber:52
    ?                        ^
    + InStackPositionNumber:53
    ?                        ^
    - InstanceNumber:100
    ?                  ^
    + InstanceNumber:101
    ?                  ^
      ...
    - SOPInstanceUID:1.2.826.0.1.3680043.8.498.10904131910506455574025613086762249469
    + SOPInstanceUID:1.2.826.0.1.3680043.8.498.39056959140773619321268443511349211124
      ...
    - SliceLocation:-30.9865036
    ?                   ^     ^
    + SliceLocation:-30.38650131
    ?                   ^    + ^
      ...
    - WindowCenter:1172
    ?                ^^
    + WindowCenter:1148
    ?                ^^
    - WindowWidth:2344
    ?              ^^^
    + WindowWidth:2297
    ?              ^^^
    ```

### 2021/08/10

- [Create 3D NPZ & TFRecords – RSNA – Radiogenomics](https://www.kaggle.com/dschettler8845/create-3d-npz-tfrecords-rsna-radiogenomics)
  - [2021/08/10 Brain Tumor - Code Kata | Kaggle](https://www.kaggle.com/mstkmyhr/2021-08-10-brain-tumor-code-kata/edit) で写経する
  - `2 SETUP` まで完了、`3 HELPER FUNCTIONS` から
- [🧠🧬 EDA+3D-Baseline – RSNA – Glioma Radiogenomics](https://www.kaggle.com/dschettler8845/eda-3d-baseline-rsna-glioma-radiogenomics/notebook)

