def to_faa(kgenome):
    faa_features = []
    
    for feature in kgenome['features']:
        faa_features.append('>' + feature['id'] + '\n' + feature['protein_translation'])
        #print(feature)
        #break
    
    return '\n'.join(faa_features)