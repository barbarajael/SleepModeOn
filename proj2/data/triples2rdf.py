# Formato RDF N-Triples (NT)
# Todos os sujeitos e predicados são URIs, todos os objetos são literais

import csv

csv_file = open("sleepdata_triples.csv", 'r', encoding='utf-8')
rdf_file = open("sleepdata_rdf.nt", "w", encoding='utf-8')
reader = csv.reader(csv_file)

for suj, pred, obj in reader:
    rdf_suj = str("<http://sleepdata.com/entity/" + suj.replace(" ", "_") + ">")      # Não podem existir espaços em branco no URI
    rdf_pred = str("<http://sleepdata.com/predicate/" + pred.replace(" ", "_") + ">")
    rdf_obj = str("\"" + obj + "\"")   # Neste conjunto de dados os objetos são todos literais, caso contrário teríamos de
                                       # encontrar um padrão de literais e sujeitos/predicados e fazer um parse
    rdf_file.write(rdf_suj + " " + rdf_pred + " " + rdf_obj + " .\n")

csv_file.close()
rdf_file.close()
