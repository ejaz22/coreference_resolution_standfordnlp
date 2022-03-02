from pycorenlp import *
# to start Stanford Core NLP server : cp <stanford_core_nlp_folder>
# java -mx6g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -timeout 10000

class ResolveCoref:
    """
    Resolve coreference using Standford NLP
    uri = "http://localhost:9000/"
    """

    def __init__(self,url="http://localhost:9000/"):
        self.nlp = StanfordCoreNLP(url)
        self.properties = {
            'annotators': 'dcoref',
            'outputFormat': 'json',
            'ner.useSUTime': 'false'
        }

    def resolve(self,text:str):
        output = self.nlp.annotate(text,self.properties)
        if type(output) is str or type(output) is unicode:
            output = json.loads(output, strict=False)
        output = self._process(output)
        return self._coref_resolve(output)

    def _process(self, corenlp_output):
        for coref in corenlp_output['corefs']:
            mentions = corenlp_output['corefs'][coref]
            antecedent = mentions[0]
            for j in range(1, len(mentions)):
                mention = mentions[j]
                if mention['type'] == 'PRONOMINAL':
                    target_sentence = mention['sentNum']
                    target_token = mention['startIndex'] - 1
                    corenlp_output['sentences'][target_sentence - 1]['tokens'][target_token]['word'] = antecedent['text']
        return corenlp_output

    def _coref_resolve(self, corenlp_output):
        resolved_text = []
        possessives = ['hers', 'his', 'their', 'theirs']
        for sentence in corenlp_output['sentences']:
            for token in sentence['tokens']:
                resolved_text.append(token['word'])
                if token['lemma'] in possessives or token['pos'] == 'PRP$':
                    resolved_text.append("'s")
                resolved_text.append(token['after'])
        return ''.join(resolved_text)
      
  if __name__ = "__main__":
    obj = ResolveCoref()
    s='Caroline is a talented girl. She loves eggs. Her dog is Bruno'
    obj.resolve(s)
    "Caroline is a talented girl. Caroline loves eggs. Caroline's dog is Bruno"
