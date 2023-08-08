import os
import signal
import subprocess
import warnings

from utils import ontoumlimport, command, generateinput, gspanMiner, back2uml, graphClustering1, uml_viz

directory_path = './models'  # replace with the path to your directory
extension = '.json'  # replace with the desired file extension
patternspath = "input/outputpatterns.txt"  # replace with patterns file name
uml_folder = "./patterns"
plantuml_jar_path = "plantumlGenerator.jar"
node_labels0 = ["gen", "characterization", "comparative", "externalDependence", "material", "mediation",
                "componentOf", "memberOf", "subCollectionOf", "subQuantityOf", "bringsAbout",
                "creation", "historicalDependence", "manifestation", "participation",
                "participational", "termination", "triggers", "instantiation", "relation"]
edge_labels0 = ["target", "specific", "general", "source", "generalization"]

file_names = []
for filename in os.listdir(directory_path):
    if filename.endswith(extension):
        file_names.append(filename)

if __name__ == "__main__":

    graphs = ontoumlimport.generateFullUndirected(file_names)
    class_labels = command.filterClasses()
    relation_labels = command.filterRelations()
    node_labels = class_labels + relation_labels
    edge_labels = command.filterEdges()
    newgraphs = generateinput.process_graphs(node_labels, edge_labels, graphs)
    newgraphs_with_names = generateinput.process_graphs_with_names(node_labels, edge_labels, graphs)
    # newgraphs = replace_labels_with_default(class_labels, relation_labels, edge_labels, graphs)
    downloadgraphs = generateinput.save_graphs_to_pickle(newgraphs, './input/graphs.pickle')
    data = generateinput.graphs_to_data_file(newgraphs_with_names, 'graphs')
    gsParameters = command.parameters()
    print("Baking the output... ")
    inputs = gspanMiner.gsparameters(gsParameters)


    def timeout_handler(signum, frame):
        raise TimeoutError("Function execution timed out")


    # Set the alarm signal to call the timeout_handler after 30 seconds
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(900)  # seconds
    try:
        patterns = gspanMiner.run_gspan(inputs)
    except TimeoutError:
        print("Function execution timed out")
    finally:
        signal.alarm(0)
    command.firststop()

    uploadgraphs = patterns.load_graphs_from_pickle('./input/graphs.pickle')
    pattern_graphs = patterns.convertPatterns(patternspath)
    pro_pattern_graphs = patterns.return_all_domain_info(pattern_graphs)
    # patterns_features = graphClustering.extract_features(pattern_graphs)
    patterns_features = graphClustering1.graphs2dataframes2vectors(pattern_graphs)
    # patterns_dataframe = graphClustering.transform_graph_data(patterns_features)
    patterns_dataframe = graphClustering1.transform2singledataframe(patterns_features)
    print("patterns_dataframe")
    print(patterns_dataframe)
    patterns_similarity_matrix = graphClustering1.calculate_similarity(patterns_dataframe)
    print("patterns_similarity_matrix")
    print(patterns_similarity_matrix)
    similarity_threshold = command.ask_similarity_threshold()
    patterns_cluster_labels = graphClustering1.group_similar_items(patterns_similarity_matrix,
                                                                   similarity_threshold)
    pattern_graphs_clustered_ = graphClustering1.merge_lists(patterns_cluster_labels, pattern_graphs)
    pattern_graphs_clustered = back2uml.process_genset_cardinalities(pattern_graphs_clustered_)
    converted_patterns = back2uml.convert_graphs_new(pattern_graphs_clustered)
    # patterns_cluster_viz = convert_to_plantuml_clusters(pattern_graphs_clustered)

    converted_patterns_filtered = generateinput.process_graphs__(node_labels0, edge_labels0, converted_patterns)
    uml_viz.convert_to_plantuml_clusters(converted_patterns_filtered)
    warnings.filterwarnings("ignore")

    # Iterate over subfolders in the uml folder
    for root, dirs, files in os.walk(uml_folder):
        for dir in dirs:
            subfolder_path = os.path.join(root, dir)
            cmd = f"java -jar {plantuml_jar_path} {subfolder_path}"
            subprocess.run(cmd, shell=True, check=True)

    command.secondstop()
    command.process_pattern(pro_pattern_graphs, uploadgraphs, converted_patterns_filtered)
    command.laststop()
