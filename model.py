#!/usr/bin/env python
# -*-coding:utf-8 -*-
import spacy

nlp = spacy.load('en_core_web_sm')


def audio_recognition(file):
    result = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer leo nisl, bibendum sed lectus nec, laoreet finibus diam. Suspendisse commodo est nec commodo fermentum. Pellentesque facilisis finibus elementum. Aenean ultrices, justo id luctus scelerisque, lorem dui egestas purus, vitae feugiat est ipsum a nisi. Maecenas malesuada tincidunt diam vel suscipit. Fusce laoreet euismod velit. Donec pulvinar sagittis felis at tristique. Praesent massa diam, auctor a enim vel, tristique commodo justo. Quisque rutrum aliquam enim, at mattis ipsum ultricies eget. Donec at nibh risus. Nunc consequat convallis libero, sit amet pulvinar quam porttitor sed.
Morbi tempor lacinia mi id accumsan. Nullam eget lacus mi. Aenean sed erat eu risus pellentesque malesuada. Curabitur sit amet eleifend quam, nec ultrices ante. Curabitur porttitor in tellus vitae sagittis. Praesent faucibus elementum est, eget pellentesque ante egestas eu. Suspendisse non convallis neque. Nunc sit amet ex vitae nisl placerat scelerisque. Mauris volutpat metus sed molestie porta. Mauris facilisis viverra erat, auctor cursus libero ullamcorper eu. Donec sagittis efficitur velit et volutpat.
In turpis orci, pharetra at tortor tincidunt, varius efficitur nunc. Cras varius auctor turpis, eget cursus magna iaculis et. Pellentesque egestas sapien justo, quis fermentum sapien euismod id. Etiam quis justo ex. In id purus ipsum. Aenean volutpat orci tellus, non cursus justo tempus eget. Phasellus aliquam justo et mi malesuada lobortis. Proin lacus est, malesuada id pulvinar quis, posuere ac lorem. Nulla non rutrum dui, id faucibus lectus. Curabitur tempor lacus vitae volutpat imperdiet.
Duis aliquet pharetra diam ac faucibus. Nunc ac semper quam. Aenean sit amet sem sit amet enim vestibulum sagittis. Aenean eu suscipit ex. Integer suscipit magna lectus, ut aliquam nunc dapibus sit amet. Suspendisse potenti. Sed neque nulla, volutpat vitae dictum in, accumsan nec nisi. Etiam aliquam congue tellus a ullamcorper. Nunc vel dolor venenatis, elementum arcu a, euismod dolor. Vivamus hendrerit arcu id sagittis iaculis.
Nulla viverra feugiat tortor et commodo. Morbi efficitur quis elit sed pulvinar. Nullam non faucibus nisl. Aliquam ultricies suscipit elit, nec pulvinar ex venenatis id. Praesent egestas enim non dolor malesuada convallis. Cras nibh elit, condimentum non convallis a, pharetra vel diam. Quisque vel ante pretium, gravida ipsum nec, pretium erat.
""".strip()
    doc = nlp(result)
    tokens = []
    for token in doc:
        if token.whitespace_:
            tokens.append({'text': token.text, 'pos': token.pos_})
            tokens.append({'text': ' ', 'pos': 'SPACE'})
        else:
            tokens.append({'text': token.text, 'pos': token.pos_})
    return {"text": result, "tokens": tokens}
