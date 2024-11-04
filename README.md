# Open Science AI Toolkit
Open source suite of tools, workflows, and processes designed to accelerate Open Science AI/ML development.

### Overview
```mermaid
flowchart LR
  ABC[Data Preparation] --> D[Model Training]
  D --> E[Model Evaluation]
  E --> F{Satisfactory Performance?}
  F -->|Yes| G[Model Deployment]
  F -->|No| D
  G --> H[Model Monitoring]
  H --> ABC
```

### Notebooks
A collection of Jupyter notebooks for different stages of the AI/ML pipeline:

| Category                                         | Notebook Name                                      | Description                                                                               | Deploy  | 
| ------------------------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------|
| Data Preparation                                  | **Data Prep**                                      | Prepares training and testing datasets, and verifies metadata                             | placeholder| 
| Model Training                                    | **Train YOLO11 Model**                            | Configures parameters and trains YOLOv11 models                                           | placeholder  | 
| Model Training                                    | **Train YOLO11 Segment Model**                    | Configures parameters and trains YOLOv11 segmentation models                              | placeholder | 
| Model Training                                    | **Train YOLOv8 Model**                             | Configures parameters and trains YOLOv8 models                                            |placeholder| 
| Model Evaluation                                  | **Evaluate Models**                                | Generates metrics and performs comprehensive model testing                                | placeholder|
| Model Deployment                                  | **Publish Models**                                 | Publishes trained models to public repositories for community access                       | placeholder  | 

### Scripts
*Placeholder for various scripts that automate critical tasks.*

### Apps
*Placeholder for applications that streamline workflows.*
----------
#### Disclaimer
This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project content is provided on an ‘as is’ basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.

##### License
See the [LICENSE.md](./LICENSE.md) for details
