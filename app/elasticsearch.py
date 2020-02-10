#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:45:21 2019

@author: epikt
"""
from app.models import  Event
import json
#from app import elasticsearch

#def export_to_elasticsearch:
def get_participant_list(participants):
    participants_list=[]
    if participants:
        for participant in participants:
            try:
                participants_list.append({
                        "participant_id" : participant.id,
                        "paticipant_first_name" : participant.person.first_name if participant.person else None,
                        "paticipant_last_name" : participant.person.last_name if participant.person else None,
                        "participant_gender" : participant.person.gender.name if participant.person else None,
                        "participant_nationalities" : [ n.name for n in participant.person.nationalities ] if participant.person else [],
                        "paticipant_activity" : participant.activity.name if participant.activity else None,
                        "paticipant_instrument" : (participant.activity.instrument.name if participant.activity.instrument else None ) if participant.activity else None,
                        "paticipant_musical_ensemble" : participant.musical_ensemble.name if participant.musical_ensemble else None })
            except Exception as ex:
                print(participant)
                raise ex
    return participants_list
 
def get_events_json():
    """Get the high level json for exporting to ES"""
    events=Event.query.all()
    json_events=[]
    try:
        for event in events:
            json_event={}
            json_event["event_id"] = event.id
            json_event["event_name"] = event.name
            json_event["location_name"] = event.location.name
            json_event["location_city"] = event.location.city.name
            json_event["event_organizations"] = [ org.name for org in event.organizations ] 
            json_event["event_type"] = event.event_type.name
            json_event["event_cycle"] = event.cycle.name
            json_event["event_date_day"] = event.day
            json_event["event_date_month"] = event.month
            json_event["event_date_year"] = event.year
            json_event["event_information"] =  event.information
            json_event["media_links"] = [{ "medialink_name": ml.filename, "medialink_description": ml.description } for ml in event.medialinks] 
            json_event["participants"] = get_participant_list(event.participants.all())
            json_event["performances"]: [ { 
                    "performance_id" : performance.id,
                    "premiere" : performance.premiere_type.name,
                    "musical_piece_name" 	: performance.musical_piece.name,
                    "composers": [ { 
                            "composer_first_name" : composer.first_name,
                            "composer_last_name" : composer.last_name,
                            "composer_nationalities" : [nationality.name  for nationality in composer.nationalities]    }
                            for composer in performance.musical_piece.composers ],
                    "participants" : get_participant_list(performance.get_participant_list)
                    }
                    for performance in event.performances.all()     ]
            json_events.append(json_event)
    except Exception as ex:
        print(event.id)
        raise ex
    with open('events.json', 'w') as fp:
        json.dump(json_events, fp)


""""
event
{
    "event_id":1,
    "event_name": "Concierto para piano Fausto García Medeles",
    "event_location_name": "Embajada de México",
    "event_location_city": "Santiago",
    "event_organizations": [  "Embajada de México" , "Instituto de Artes Mexicanas"],
    "event_type": "Concierto",
    "event_cycle" : "Conciertos de Verano Mexico",
    "event_date_day" : 21,  # puede ser nulo
    "event_date_month" : 5,  # puede ser nulo
    "event_date_year" : 1980,
    "event_information" : "a long text here, up to 4000 characters",
    "media_links" : [ { "medialink_name": "/data/media/file.txt", "medialink_description": "un archivo de texto" }, 
    				  { "medialink_name": "/data/media/file.mp3", "medialink_description": "un archivo de audio" } ],
    "participants" : [ { 
    					 "participant_id"        : 1,
    					 "paticipant_first_name" : "Claudio", # puede ser nulo
    					 "paticipant_last_name"  : "Gonzalez", # puede ser nulo. En algunos caso es nulo el lastname, en otro el firstname
    					 "participant_gender"	 : "Hombre",
    					 "participant_nationalities" : [ "Argentina", "Chile"],
    					 "paticipant_activity"   : "Pianista",
    					 "paticipant_instrument" : "Piano",
    					 "paticipant_musical_ensemble" : "Orquesta Dingdong"
    					  },
						{ 
						 "participant_id"		 : 2,
						 "paticipant_first_name" : "Laura",
    					 "paticipant_last_name"  : "Meza",
    					 "participant_gender"	 : "Mjer",
    					 "participant_nationalities" : [  "Chile"],
    					 "paticipant_activity"   : "Cantante",
    					 "paticipant_instrument" : "Ninguno",
    					 "paticipant_musical_ensemble" : ""
    					}    					  
    				],
    "performances" : [ {
    					"performance_id" 		: 1,
    					"premiere" 				: "No",
    					"musical_piece_name" 	: "El lago de los patos",
    					"composer_first_name"   : "Ludovico",
    					"componer_last_name"    : "Elbato",
    					"componser_nationalities" : ["Suecia","Austria"],
    					"musical_piece_composition_year" : 1822,
    					# existe un 'tipo de instrumento', si se quiere buscar por el tipo de instrumento, la lista de
    					# musical_piece_instruments tendría que ser una lista de objetos en vez de strings, lo que hará más
    					# complejos los queries 
    					"musical_piece_instruments" : ["Piano", "Violín"], 
    					"musical_piece_instrumental_lineup" : "Dúo" 
    					},
    					{
    					"performance_id" 		: 2,
    					"premiere" 				: "Estreno en Chile",
    					"musical_piece_name" 	: "El lago de los perros",
    					"composer_first_name"   : "Pionino",
    					"componer_last_name"    : "Turimbato",
    					"componser_nationalities" : ["Italia"],
    					"musical_piece_composition_year" : 1722,
    					"musical_piece_instruments" : [],
    					"musical_piece_instrumental_lineup" : "" 
    					}
    				],
    # este hace el cruce de los el performace y quién participó en ella. Es bastante usual que esta lista esté vacía
    "participant_performance" : [ { "participant_id" : 1, "performance_id" : 1 } , 
    							  { "participant_id" : 1, "performance_id" : 2 }]
 }

"""