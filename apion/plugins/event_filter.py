from collections import OrderedDict

class EventFilter(object):
    def __init__(self, events, playbook_name):
        self._events = events
        #self._playbook_name = playbook_name
        self._playbook_name = "run.yaml"

    def filter(self):

        if self._playbook_name in ["rmbp"]:
            res = []
            res.append(self._events)
            # for event in self._events:
            #     res.append(event)
            #     if event["event"] == "runner_on_ok":
            #         # nevent = {event["event_data"]["task_action"]: {
            #         #     "before": event['event_data']['res']['before'],
            #         #     "after": event['event_data']['res'].get('after', None),
            #         #     "commands": event['event_data']['res']['commands'],
            #         #     "changed": event['event_data']['res']['changed'],
            #         #     "status": "ok"
            #         # }}
            #         res.append(event)

                # if event['event'] == "runner_on_failed":
                #     # nevent = {event["event_data"]["task_action"]: {
                #     #     "msg": event['event_data']['res']['msg'],
                #     #     "status": "failed"
                #     # }}
                #    res.append(event)
            print("RESULT ------------", res)
            return {"results": res}