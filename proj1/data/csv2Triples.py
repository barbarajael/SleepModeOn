import csv

orig = open("sleepdata.csv", "r", encoding="utf-8") # Conjunto de dados no formato original
reader = csv.reader(orig)

next(reader, None)  # Remoção do cabeçalho

sleepdata_without_empty_lines = open("sleepdata_without_empty_lines.csv", "w", encoding="utf-8", newline='')  # Remoção de linhas vazias
writer = csv.writer(sleepdata_without_empty_lines)
for row in reader:
    if row:
        writer.writerow(row)
orig.close()
sleepdata_without_empty_lines.close()

sleepdata_without_empty_lines = open("sleepdata_without_empty_lines.csv", "r", encoding="utf-8")
reader = csv.reader(sleepdata_without_empty_lines, delimiter=';')

sleepdata_triples = open("sleepdata_triples.csv", "w", encoding="utf-8", newline='')  # Formato de triplos (sujeito - predicado - valor)
writer = csv.writer(sleepdata_triples)
i = 1
for start, end, quality, time_in_bed, feeling, notes, heart_rate, steps in reader:
    id = 's' + str(i)
    if start: # If the variable "start" is not empty
        writer.writerow([id, 'start', start])
    if end:
        writer.writerow([id, 'end', end])
    if quality:
        writer.writerow([id, 'quality', quality])
    if time_in_bed:
        writer.writerow([id, 'time_in_bed', time_in_bed])
    if feeling:
        writer.writerow([id, 'feeling', feeling])
    if notes:
        writer.writerow([id, 'notes', notes])
    if heart_rate:
        writer.writerow([id, 'heart_rate', heart_rate])
    if steps:
        writer.writerow([id, 'steps', steps])
    i = i + 1
sleepdata_without_empty_lines.close()
sleepdata_triples.close()
