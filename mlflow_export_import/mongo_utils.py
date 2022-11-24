import json
import os

from pymongo import MongoClient
from bson.objectid import ObjectId

def get_domino_env(envs):

    for e in envs:
        if 'dominodatalab/environment' in e:
            idx = e.rindex(':')
            env = e[idx+1:]
            idx_2 = env.rindex('-')
            env_id = env[:idx_2]
            env_version = env[idx_2+1:]
            return env_id,revisions_by_key[env]
    return '',''
envs_by_revision={}
def get_env(env_coll,env_revision_id):
    if not env_revision_id in envs_by_revision:
        objInstance = ObjectId(env_revision_id)
        env = env_coll.find_one({"_id": objInstance})
        if env:
            envs_by_revision[env_revision_id] = {'environmentId':str(env['environmentId']), "env_revision_id":env_revision_id}
    return  envs_by_revision[env_revision_id]


revisions_by_key = {}
def get_runs(mongo_url):
    runs_by_id = {}
    mongodb_client = MongoClient(mongo_url)
    database = mongodb_client['domino']
    print("Connected to the MongoDB database!")
    sagas = database.sagas  # choosing the collection you need
    environment_revisions = database.environment_revisions

    for document in environment_revisions.find():
        env_id = str(document['environmentId']) + "-" + str(document['metadata']['number'])
        revisions_by_key[env_id]=str(document['_id'])

    for document in sagas.find():
        doc = json.loads(document['parameterJson'])
        if ('runId' in doc or 'containerImagesPulled' in doc):
            if doc['containerImagesPulled']:
                #print(k['containerImagesPulled'])
                env_id,env_revision_id  = get_domino_env(doc['containerImagesPulled'])
                runs_by_id[doc['runId']] = {'env_id': env_id, 'env_revision_id' : env_revision_id, 'run_type': doc['runType'] }

    runs = database.runs  # choosing the collection you need

    for document in runs.find():
        environment = get_env(environment_revisions,document['environmentRevisionId'])

        runs_by_id[document['_id']] = {'env_id': environment['environmentId'],
                                       'env_revision_id': str(document['environmentRevisionId']),
                                       'hardware_tier': document['executionClass']['name'],
                                       'run_number' : document['number']}
        if 'labels' in document['volumeSpecification']:
            for l in document['volumeSpecification']['labels']:
                if l['key']=='dominodatalab.com/type':
                    runs_by_id[document['_id']]['run_type'] = l['value']

    return runs_by_id

if __name__ == "__main__":
    MONGO_HOSTNAME = os.environ.get('MONGO_HOSTNAME', '')
    MONGO_PORT = os.environ.get('MONGO_PORT', 'MONGO_PORT')
    MONGO_USER_ID = os.environ.get('MONGO_USER_ID', '')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD', '')
    MONGO_URL = f'mongodb://{MONGO_USER_ID}:{MONGO_PASSWORD}@{MONGO_HOSTNAME}:{MONGO_PORT}/?authMechanism=DEFAULT&directConnection=true'
    print(MONGO_URL)
    runs = get_runs(MONGO_URL)


    #with open("", "w") as outfile:
        #json.dump(runs, outfile)
    for key, value in runs.items():
        print(key, '->', value)