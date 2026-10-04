from resilientcity.graph import build_graph
from resilientcity.models import Incident
def test_graph_requires_human_review_when_road_unknown():
    i=Incident(incident_id='T-03',location='Central Avenue',description='Heavy rain with unverified road condition.',rainfall_mm=70,road_status='unknown'); r=build_graph().invoke({'incident':i.model_dump(),'revision_count':0,'trace':[]}); assert r['safety']['status']=='HUMAN_REVIEW_REQUIRED'; assert r['revision_count']==1; assert 'Humans decide' in r['final_report']
