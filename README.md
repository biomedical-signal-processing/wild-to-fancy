# wild-to-fancy

The `wild-to-fancy` repository provides tools for harmonizing polysomnography (PSG) datasets, enabling seamless conversion into formats suitable for advanced sleep staging analysis. This project builds upon the original [U-Time](https://github.com/perslev/U-Time) repository, incorporating its harmonization principles to adapt diverse datasets into a standardized structure.


## Overview

This repository is part of the **wild-to-fancy** service within the larger [SLEEPYLAND](https://github.com/biomedical-signal-processing/SLEEPYLAND) project. The primary purpose of this service is to:

**Harmonize NSRR Datasets**:
   - Process uploaded datasets, specifically `.edf` and annotation files (e.g., `.xml`), and standardize them into a consistent format.
   - Organize the harmonized output files into the appropriate directory structure for downstream analysis within SLEEPYLAND or standalone workflows.

## Usage and Deployment

The repository can be used as part of SLEEPYLAND or as a standalone utility.

### Standalone Docker Deployment

The service is available as a Docker image for easy deployment in [Docker Hub](https://hub.docker.com/repository/docker/bspsupsi/sleepyland/general):
```bash
docker pull bspsupsi/sleepyland:wild-to-fancy
docker run -v /path/to/data:/data bspsupsi/sleepyland:wild-to-fancy
```

This containerized version ensures a consistent and reliable environment for running the service across various systems.

## Acknowledgments

The original [U-Time](https://github.com/perslev/U-Time) repository serves as the basis for this work. We acknowledge the foundational contributions of its authors. This revised version builds upon their efforts to expand its capabilities within the SLEEPYLAND project.

---

For any issues, feature requests, or contributions, please submit a pull request or create an issue in this repository or the [SLEEPYLAND](https://github.com/biomedical-signal-processing/SLEEPYLAND) repository.