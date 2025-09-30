import csv

tsv_path = './resources/groundings_50_v1.tsv'

tp = fp = fn = tn = 0

with open(tsv_path, newline='') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        gt = row['cl_id']
        pred = row['grounding_cl_id']
        if gt == pred and gt != '':
            tp += 1
        elif gt != pred and pred != '':
            fp += 1
        elif gt != pred and pred == '':
            fn += 1
        elif gt == '' and pred == '':
            tn += 1

precision = tp / (tp + fp) if (tp + fp) else 0
recall = tp / (tp + fn) if (tp + fn) else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0

print(f'Truth table: TP={tp}, FP={fp}, FN={fn}, TN={tn}')
print(f'Precision: {precision:.3f}')
print(f'Recall: {recall:.3f}')
print(f'F1 score: {f1:.3f}')