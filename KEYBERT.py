import os
from keybert import KeyBERT

def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


#implicit()

file_path = "/home/cs474/CS474/data/data.txt"

preprocessed_file = open(file_path, 'r')
file_read = preprocessed_file.read()
preprocessed_file.close()
spl = file_read.split('\n')


text = """
            s.korean envoy dismisses china concern you. s. missile defense s.korean ambassador china kim jang-soo dismissed beijing concerns usa ay possible deployment advanced you. s. missile-defense system s.korea saying n.korea nuclear missile arsenals pose threats seoul beijing. better cope gro threats n.korea nuclear missile capabilities s.korean you. s. officials indicated need terminal high-altitude area defense battery s.korea. arguing you. s. missile-defense system could also target china beijing publicly pressed seoul accept thaad battery. return s.korea defense ministry blamed china trying influence seoul security policy. fundamental reason debates possible deployment thaad s.korea continue n.korea contin usa advance nuclear missile capabilities kim said intervie hong kong-based phoenix television. kim said n.korea building security unrest situation serving security strategic interests s.korea china. october s.korean defense minister han min-koo told la s deploying thaad battery you. s. military base s.korea help defend n.korea missile nuclear threats. s.korea home 28 500 american troops. chinese scholars say radar thaad system monitor objects located deep inside chinese mainland. ho kim former defense minister headed national security council presidential office cheong wa dae said china need certain limit radar thaad system. kim elaborate further. s.korea you. s. called china economic lifeline n.korea rein n.korea nuclear missile programs china stance ideological ally pyongyang often self-contradictory. many analysts believe china ruling communist party leadership put enough pressure n.korea give nuclear ambitions sudden collapse north regime could threaten china security interests. n.korea state media reported saturday pyongyang successfully test-launched ballistic missile submarine. independently confirmed significant advance missile technology n.korea conducted three nuclear tests far.
        """


text = spl[2]

raw = """S. Korean envoy dismisses China's concern over U.S. missile defense South Korean Ambassador to China Kim Jang-soo dismissed Beijing's concerns Tuesday over the possible deployment of an advanced U.S. missile-defense system in South Korea, saying that North Korea's nuclear and missile arsenals pose threats to both Seoul and Beijing. To better cope with the growing threats of North Korea's nuclear and missile capabilities, both South Korean and U.S.officials have indicated the need for the Terminal High-Altitude Area Defense battery in South Korea. Arguing that the U.S. missile-defense system could also target China, Beijing has publicly pressed Seoul not to accept the THAAD battery. In return, South Korea's defense ministry has blamed China for trying to "influence" Seoul's security policy."The fundamental reason why debates over the possible deployment of the THAAD in South Korea continue is that North Korea continues to advance its nuclear and missile capabilities," Kim said in an interview with Hong Kong-based Phoenix television. Kim said North Korea is "building up security unrest and this situation is not serving the security and strategic interests of both South Korea and China." In October, South Korean Defense Minister Han Min-koo told lawmakers that deploying a THAAD battery at a U.S. military base in South Korea would help defend against North Korea's missile and nuclear threats. South Korea is home to about 28,500 American troops. Chinese scholars say the radar of the THAAD system can monitor objects located deep inside the Chinese mainland. However, Kim, a former defense minister who headed the National Security Council at the presidential office Cheong Wa Dae, said China "does not need to be worried because there is a certain limit in the radar of the THAAD system." Kim did not elaborate further. South Korea and the U.S. have called for China, the economic lifeline of North Korea, to do more to rein in North Korea's nuclear and missile programs, but China's stance over its ideological ally, Pyongyang, has often been self-contradictory. Many analysts believe that China's ruling Communist Party leadership won't put enough pressure on North Korea to give up its nuclear ambitions because a sudden collapse of the North's regime could threaten China's own security interests.North Korea's state media reported on Saturday that Pyongyang has successfully test-launched a ballistic missile from a submarine.If independently confirmed, it would be a significant advance in the missile technology of North Korea, which has conducted three nuclear tests so far. (Yonhap)
"""

raw_1 = """Park renews calls for civil service pension reform President Park Geun-hye called Tuesday for the swift passage of a bill to overhaul civil service pensions, warning that the issue could become a ticking "time bomb" unless addressed.South Korea has faced the looming crisis as previous governments delayed addressing the issue of pensions for civil servants, despite being aware for decades that the current pension plan is not sustainable.The case for pension reform for public servants has gained urgency as the increasing average life expectancy for Koreans could further deepen the pension deficit.Park said any delay in reforming civil service pensions could worsen the public's burden, noting that politicians should never leave behind a legacy of debt for future generations.Park said the pension "time bomb could explode" unless the political community and the government address the issue.She has warned that by next year the government will be forced to use 10 billion won ($9 million) of taxpayer money every day to fund the civil service pensions unless the parliament passes a reform bill by early May. (Yonhap)
"""

text = raw_1
#print(text, '\n')

kw_model = KeyBERT()
# keywords = kw_model.extract_keywords(raw, keyphrase_ngram_range = (1, 2), stop_words=None)
keywords = kw_model.extract_keywords(text, keyphrase_ngram_range = (1, 10), stop_words=None)
print(keywords)


#for keyword in keywords:
#    print()

## pip install googletrans==4.0.0-rc1
#from googletrans import Translator
'''
translator = Translator()
for k, p in keywords:
    keywords_ko = translator.translate(k,           dest='ko', src='en').text
    keywords_en = translator.translate(keywords_ko, dest='en', src='ko').text
    print(f'{p}: {k} -> {keywords_ko} -> {keywords_en}')
'''

'''
translator = Translator(service_urls = ["papago.naver.com"])
for k, p in keywords:
    keywords_ko = translator.translate(k,           dest='ko', src='en').text
    keywords_en = translator.translate(keywords_ko, dest='en', src='ko').text
    print(f'{p}: {k} -> {keywords_ko} -> {keywords_en}')
'''