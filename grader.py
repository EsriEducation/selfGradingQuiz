# Normally, this would be used as an Amazon Lambda or Google Cloud Function
# remove the main at bottom.

from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
serviceid=0

# function takes in serviceid (as URL param and then grades. Use standard Q1-Q8. Correct responses value =a.)
# use Integromat or Flow to create URL param from S123

def core(request):
    # must convert the service id passed in URL to the corresponding fieldworker service
    if request.args and "id" in request.args:
        fieldworker = request.args["id"]
        if fieldworker == 'e51735cf5cc648d2952ce6363104f143':
            serviceid = '6e198484fc704e3cb084a410de90e372'
        else:
            serviceid='0'
        #return serviceid
    else:
        return 'no id'

    # script will need to turn off tracking and turn on in order for changes
    gis = GIS("https://xxxxx.maps.arcgis.com", "", "")
    GCK = gis.content.search("id:"+serviceid)

    # access the collection's  layers
    users_item = GCK[0]  # hosted feature layer (collection)
    users_layers = users_item.layers  # list obj

    # edit the feature service record
    users_fset = users_layers[0].query()  # feature set obj
    users_features = users_fset.features  # list obj
    users_flayer = users_layers[0]  # users_flayer is the 'survey' point layer

    # SET FEATURE LAYER COLLECTION PROPERTIES ON/OFF
    # capabilities "Update" tied to the 'who' switch in UI
    update_dict = {"capabilities": "Query, ChangeTracking, Editing",
                "editorTrackingInfo": {
                    "allowOthersToDelete": False,
                    "allowOthersToQuery": False,
                    "enableOwnershipAccessControl": True,
                    "enableEditorTracking": False,
                    "allowOthersToUpdate": False}
                }
    update_dict2 = {"capabilities": "Query, Editing, Create, Update",
                "editorTrackingInfo": {
                    "allowOthersToDelete": False,
                    "allowOthersToQuery": False,
                    "enableOwnershipAccessControl": True,
                    "enableEditorTracking": True,
                    "allowOthersToUpdate": False}
                }
    # Feature layer collection dive
    myCollection_flc = FeatureLayerCollection.fromitem(users_item)
    myCollection_flc.manager.update_definition(update_dict)

    for x in range(0, len(users_features)):
        OneRecord_feature = [f for f in users_features if (1 == 1)][x]
        # if record has already been processed, skip it.
        myProcessed = OneRecord_feature.attributes['Processed']
        if myProcessed is not 1:
            # assign table values to local vars for processing
            myCreator = OneRecord_feature.attributes['Creator']
            teacher = OneRecord_feature.attributes['teachers_ago_username']
            Q1 = OneRecord_feature.attributes['Q1']
            Q2 = OneRecord_feature.attributes['Q2']
            Q3 = OneRecord_feature.attributes['Q3']
            Q4 = OneRecord_feature.attributes['Q4']
            Q5 = OneRecord_feature.attributes['Q5']
            Q6 = OneRecord_feature.attributes['Q6']
            Q7 = OneRecord_feature.attributes['Q7']
            Q8 = OneRecord_feature.attributes['Q8']
            print('Updating quiz data for: ', teacher)
            total_correct = 0
            percent_correct = 0
        # grade quiz
            if Q1.strip() == 'a':
                Q1 = 'Correct'
                total_correct = total_correct + 1
            else:
                Q1 = 'Incorrect'
            if Q2.strip() == 'a':
                Q2 = 'Correct'
                total_correct = total_correct + 1
            else:
                Q2 = 'Incorrect'
            if Q3.strip() == 'a':
                Q3 = 'Correct'
                total_correct = total_correct + 1
            else:
                Q3 = 'Incorrect'
            if Q4.strip() == 'a':
                Q4 = 'Correct'
                total_correct = total_correct + 1
            else:
                Q4 = 'Incorrect'
            if Q5.strip() == 'a':
                Q5 = 'Correct'
                total_correct = total_correct + 1
            else:
                Q5 = 'Incorrect'
            if Q6.strip() == 'a':
                Q6 = 'Correct'
                total_correct = total_correct + 1
            else:
                Q6 = 'Incorrect'
            if Q7.strip() == 'a':
                Q7 = 'Correct'
                total_correct = total_correct + 1
            else:
                Q7 = 'Incorrect'
            if Q8.strip() == 'a':
                Q8 = 'Correct'
                total_correct = total_correct + 1
            else:
                Q8 = 'Incorrect'

            percent_correct = (total_correct / 8) * 100

        # set up edit
            OneRecord_edit = OneRecord_feature
            OneRecord_edit.attributes['Creator'] = teacher
            OneRecord_edit.attributes['Processed'] = 1
            OneRecord_edit.attributes['Q1'] = Q1
            OneRecord_edit.attributes['Q2'] = Q2
            OneRecord_edit.attributes['Q3'] = Q3
            OneRecord_edit.attributes['Q4'] = Q4
            OneRecord_edit.attributes['Q5'] = Q5
            OneRecord_edit.attributes['Q6'] = Q6
            OneRecord_edit.attributes['Q7'] = Q7
            OneRecord_edit.attributes['Q8'] = Q8
            OneRecord_edit.attributes['total_correct'] = total_correct
            OneRecord_edit.attributes['percent_correct'] = percent_correct
        # commit update
            update_result = users_flayer.edit_features(updates=[OneRecord_edit])
    # reset table permissions to original   
    myCollection_flc.manager.update_definition(update_dict2)
    return 'ok'

  if __name__ == "__main__":
    core()
