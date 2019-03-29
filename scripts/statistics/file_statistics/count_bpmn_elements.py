from src_bpmn_crawler.db_handler import DbHandler
import xmltodict
import os
import numpy as np


all_files_path = "data_GH_projects/all_files"
db_path = "data_GH_projects/databases/result.db"
table_res_bpmn = "result_bpmn"
db_handler = DbHandler()
db_conn = db_handler.create_connection(db_path)

process_names_list = ["process", "bpmn2:process", "bpmn:process", "semantic:process"]

elements_events = [["startEvent", "endEvent", "intermediateCatchEvent",
                    "intermediateThrowEvent", "boundaryEvent", "terminateEventDefinition",
                    "compensateEventDefinition", "conditionalEventDefinition",
                    "errorEventDefinition", "error", "escalationEventDefinition", "escalation",
                    "messageEventDefinition", "message", "signalEventDefinition",
                    "timerEventDefinition"],

                   ["bpmn2:startEvent", "bpmn2:endEvent", "bpmn2:intermediateCatchEvent",
                    "bpmn2:intermediateThrowEvent", "bpmn2:boundaryEvent", "bpmn2:terminateEventDefinition",
                    "bpmn2:compensateEventDefinition", "bpmn2:conditionalEventDefinition", "bpmn2:errorEventDefinition",
                    "bpmn2:error", "bpmn2:escalationEventDefinition", "bpmn2:escalation", "bpmn2:messageEventDefinition",
                    "bpmn2:message", "bpmn2:signalEventDefinition", "bpmn2:timerEventDefinition"],

                   ["bpmn:startEvent", "bpmn:endEvent", "bpmn:intermediateCatchEvent",
                    "bpmn:intermediateThrowEvent", "bpmn:boundaryEvent", "bpmn:terminateEventDefinition",
                    "bpmn:compensateEventDefinition", "bpmn:conditionalEventDefinition", "bpmn:errorEventDefinition",
                    "bpmn:error", "bpmn:escalationEventDefinition", "bpmn:escalation", "bpmn:messageEventDefinition",
                    "bpmn:message", "bpmn:signalEventDefinition", "bpmn:timerEventDefinition"],

                   ["semantic:startEvent", "semantic:endEvent", "semantic:intermediateCatchEvent",
                    "semantic:intermediateThrowEvent", "semantic:boundaryEvent", "semantic:terminateEventDefinition",
                    "semantic:compensateEventDefinition", "semantic:conditionalEventDefinition",
                    "semantic:errorEventDefinition", "semantic:error", "semantic:escalationEventDefinition",
                    "semantic:escalation", "semantic:messageEventDefinition", "semantic:message",
                    "semantic:signalEventDefinition", "semantic:timerEventDefinition"]]


elements_activities = [["task", "scriptTask", "script", "userTask", "potentialOwner",
                        "resourceAssignmentExpression", "businessRuleTask", "manualTask",
                        "sendTask", "receiveTask", "serviceTask", "subProcess",
                        "adHocSubProcess", "callActivity", "multiInstanceLoopCharacteristics",
                        "onEntry-script*", "onExit-script*"],

                       ["bpmn2:task", "bpmn2:scriptTask", "bpmn2:script", "bpmn2:userTask", "bpmn2:potentialOwner",
                        "bpmn2:resourceAssignmentExpression", "bpmn2:businessRuleTask", "bpmn2:manualTask",
                        "bpmn2:sendTask", "bpmn2:receiveTask", "bpmn2:serviceTask", "bpmn2:subProcess",
                        "bpmn2:adHocSubProcess", "bpmn2:callActivity", "bpmn2:multiInstanceLoopCharacteristics",
                        "bpmn2:onEntry-script*", "bpmn2:onExit-script*"],

                       ["bpmn:task", "bpmn:scriptTask", "bpmn:script", "bpmn:userTask", "bpmn:potentialOwner",
                        "bpmn:resourceAssignmentExpression", "bpmn:businessRuleTask", "bpmn:manualTask",
                        "bpmn:sendTask", "bpmn:receiveTask", "bpmn:serviceTask", "bpmn:subProcess",
                        "bpmn:adHocSubProcess", "bpmn:callActivity", "bpmn:multiInstanceLoopCharacteristics",
                        "bpmn:onEntry-script*", "bpmn:onExit-script*"],

                       ["semantic:task", "semantic:scriptTask", "semantic:script", "semantic:userTask",
                        "semantic:potentialOwner", "semantic:resourceAssignmentExpression", "semantic:businessRuleTask",
                        "semantic:manualTask", "semantic:sendTask", "semantic:receiveTask", "semantic:serviceTask",
                        "semantic:subProcess", "semantic:adHocSubProcess", "semantic:callActivity",
                        "semantic:multiInstanceLoopCharacteristics", "semantic:onEntry-script*",
                        "semantic:onExit-script*"]]

elements_gateways = [["parallelGateway", "eventBasedGateway", "exclusiveGateway", "inclusiveGateway"],

                     ["bpmn2:parallelGateway", "bpmn2:eventBasedGateway", "bpmn2:exclusiveGateway", "bpmn2:inclusiveGateway"],

                     ["bpmn:parallelGateway", "bpmn:eventBasedGateway", "bpmn:exclusiveGateway", "bpmn:inclusiveGateway"],

                     ["semantic:parallelGateway", "semantic:eventBasedGateway", "semantic:exclusiveGateway",
                      "semantic:inclusiveGateway"]]


elements_data = [["property", "dataObject", "itemDefinition", "ioSpecification", "dataInput",
                  "dataInputAssociation", "dataOutpu", "dataOutputAssociation",
                  "inputSet", "outputSet", "assignment", "formalExpression"],

                 ["bpmn2:property", "bpmn2:dataObject", "bpmn2:itemDefinition", "bpmn2:ioSpecification", "bpmn2:dataInput",
                  "bpmn2:dataInputAssociation", "bpmn2:dataOutpu", "bpmn2:dataOutputAssociation",
                  "bpmn2:inputSet", "bpmn2:outputSet", "bpmn2:assignment", "bpmn2:formalExpression"],

                 ["bpmn:property", "bpmn:dataObject", "bpmn:itemDefinition", "bpmn:ioSpecification", "bpmn:dataInput",
                  "bpmn:dataInputAssociation", "bpmn:dataOutpu", "bpmn:dataOutputAssociation",
                  "bpmn:inputSet", "bpmn:outputSet", "bpmn:assignment", "bpmn:formalExpression"],

                 ["semantic:property", "semantic:dataObject", "semantic:itemDefinition", "semantic:ioSpecification",
                  "semantic:dataInput", "semantic:dataInputAssociation", "semantic:dataOutpu",
                  "semantic:dataOutputAssociation", "semantic:inputSet", "semantic:outputSet",
                  "semantic:assignment", "semantic:formalExpression"],
                 ]

sequenceFlow = ["sequenceFlow", "bpmn2:sequenceFlow", "bpmn:sequenceFlow", "semantic:sequenceFlow"]


def count_diagr_elements(process_list, k):
    """ Elements list contains:
         n_ele_events
         n_ele_activities
         n_ele_gateways
         n_ele_data
         n_sequence_flows
    """
    elements = [0, 0, 0, 0, 0]
    for bpmn_process in process_list:
        for key in list(bpmn_process.keys()):
            if key in elements_events[k]:
                if isinstance(bpmn_process[key], list):
                    elements[0] += len(bpmn_process[key])
                    elements = np.array(elements) + np.array(count_diagr_elements(bpmn_process[key], k))
                elif isinstance(bpmn_process[key], dict):
                    elements[0] += 1
                    elements = np.array(elements) + np.array(count_diagr_elements([bpmn_process[key]], k))
            elif key in elements_activities[k]:
                if isinstance(bpmn_process[key], list):
                    elements[1] += len(bpmn_process[key])
                    elements = np.array(elements) + np.array(count_diagr_elements(bpmn_process[key], k))
                elif isinstance(bpmn_process[key], dict):
                    elements[1] += 1
                    elements = np.array(elements) + np.array(count_diagr_elements([bpmn_process[key]], k))
            elif key in elements_gateways[k]:
                if isinstance(bpmn_process[key], list):
                    elements[2] += len(bpmn_process[key])
                    elements = np.array(elements) + np.array(count_diagr_elements(bpmn_process[key], k))
                elif isinstance(bpmn_process[key], dict):
                    elements[2] += 1
                    elements = np.array(elements) + np.array(count_diagr_elements([bpmn_process[key]], k))
            elif key in elements_data[k]:
                if isinstance(bpmn_process[key], list):
                    elements[3] += len(bpmn_process[key])
                    elements = np.array(elements) + np.array(count_diagr_elements(bpmn_process[key], k))
                elif isinstance(bpmn_process[key], dict):
                    elements[3] += 1
                    elements = np.array(elements) + np.array(count_diagr_elements([bpmn_process[key]], k))
            elif key in sequenceFlow[k]:
                if isinstance(bpmn_process[key], list):
                    elements[4] += len(bpmn_process[key])
                    elements = np.array(elements) + np.array(count_diagr_elements(bpmn_process[key], k))
                elif isinstance(bpmn_process[key], dict):
                    elements[4] += 1
                    elements = np.array(elements) + np.array(count_diagr_elements([bpmn_process[key]], k))
    return elements


def compute_bpmn_complexity():
    query1 = "SELECT path_copy_bpmn_file FROM files_copy WHERE path_bpmn_file IN (SELECT path_bpmn_file FROM " + \
             table_res_bpmn + " WHERE n_sequence_flows IS NULL);"
    bpmn_names_list = db_handler.execute_query(db_conn, query1, True)
    i = 0
    for bpmn_file in bpmn_names_list:
        bpmn_path = os.path.join(all_files_path, bpmn_file[0])
        if os.path.exists(bpmn_path):
            query2 = "SELECT path_bpmn_file FROM files_copy WHERE path_copy_bpmn_file='" + \
                     bpmn_file[0] + "';"
            bpmn_path_in_db = db_handler.execute_query(db_conn, query2, True)[0][0]

            try:
                with open(bpmn_path, 'r', encoding='utf-8', errors='ignore') as myfile:
                    file_dict = xmltodict.parse(myfile.read())
                    for key in file_dict.keys():
                        for k in range(0, len(process_names_list)):
                            if process_names_list[k] in file_dict[key]:
                                process_name = process_names_list[k]
                                if isinstance(file_dict[key][process_name], list):
                                    elements_list = count_diagr_elements(file_dict[key][process_name], k)
                                else:
                                    elements_list = count_diagr_elements([file_dict[key][process_name]], k)

                                query3 = 'UPDATE result_bpmn SET n_ele_events=' + str(elements_list[0]) + \
                                         ', n_ele_activities=' + str(elements_list[1]) + \
                                         ', n_ele_gateways=' + str(elements_list[2]) + \
                                         ', n_ele_data=' + str(elements_list[3]) + \
                                         ', n_sequence_flows=' + str(elements_list[4]) + \
                                         ' WHERE path_bpmn_file="' + bpmn_path_in_db + '";'
                                db_handler.execute_query(db_conn, query3, False)
                                break
                        break
            except:
                i += 1
                print("Couldn't open file: " + bpmn_file[0])
        else:
            print("Error path doesn't exist: " + bpmn_file[0])
    print(i)


compute_bpmn_complexity()

# 'https://access.redhat.com/documentation/en-us/jboss_enterprise_brms_platform/5/html/brms_business_process_management_guide/chap-bpmn_2.0_notation#Business_Process_Model_and_Notation_BPMN_2.0_Specification'
# 'https://docs.camunda.org/manual/latest/reference/bpmn20/#symbols'
