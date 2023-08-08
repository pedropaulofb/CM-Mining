# CM-Mining: OntoUML Pattern Mining and Visualization

This repository hosts a Python script for mining and visualizing Unified Modeling Language (UML) patterns from a collection of UML models in JSON format. The script employs various utility modules for importing UML models, running graph pattern mining algorithms, clustering patterns, and generating UML diagrams using PlantUML.

## Prerequisites

Before running the script, ensure you have the following prerequisites:

- Python 3.x
- Java (for PlantUML diagram generation)
- The necessary Python packages, which can be installed using the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. Place your UML model files (in JSON format) in the `./models` directory.

2. Modify the script to configure parameters and paths according to your needs:

   - `directory_path`: Path to the directory containing UML model files.
   - `extension`: Desired file extension for UML model files.
   - `patternspath`: File path for patterns input/output.
   - `uml_folder`: Path to the folder where PlantUML diagrams will be generated.
   - `plantuml_jar_path`: Path to the PlantUML JAR file for diagram generation.
   - `node_labels0`: List of UML node labels.
   - `edge_labels0`: List of UML edge labels.

3. Run the script:

```bash
python main.py
```

## Overview of Steps

1. Import UML models and prepare data.
2. Run graph pattern mining using gSpan algorithm.
3. Cluster mined patterns using similarity analysis.
4. Generate UML diagrams for pattern clusters.

## Output

- Mined UML patterns will be saved in the `patterns` directory.
- PlantUML diagrams will be generated in the `uml` subfolders within each pattern cluster.

## Note

- The script contains timeout handling for function execution.
- Patterns are clustered based on similarity thresholds.
- Make sure to have valid Java and PlantUML configurations for diagram generation.

## Acknowledgments

This script utilizes various utility modules (imported from the `utils` package) for different tasks, including UML import, graph pattern mining, clustering, and diagram generation.

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

---

*Disclaimer: This README is generated automatically based on the provided Python script and might require adjustments and improvements for accuracy and completeness.*