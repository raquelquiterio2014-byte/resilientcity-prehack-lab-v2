from .models import *
def _t(s,m): return [*s.get('trace',[]),m]
def planner_agent(s): return {'trace':_t(s,'Planner: incident accepted; evidence and risk analysis requested.')}
def evidence_agent(s):
    i=Incident.model_validate(s['incident']); w='high' if i.rainfall_mm>=50 else 'moderate' if i.rainfall_mm>=20 else 'low'; c=i.road_status!='unknown'; e=EvidenceAssessment(weather_signal=w,road_status=i.road_status,evidence_complete=c,confidence=.90 if c else .62); return {'evidence':e.model_dump(),'trace':_t(s,f'Evidence: weather={w}, road={i.road_status}.')}
def risk_agent(s):
    e=EvidenceAssessment.model_validate(s['evidence']); l='HIGH' if e.weather_signal=='high' and e.road_status in {'flooded','closed'} else 'MEDIUM' if e.weather_signal=='high' else 'LOW'; r=RiskAssessment(level=l,rationale='Deterministic lab assessment from rainfall and road evidence.'); return {'risk':r.model_dump(),'trace':_t(s,f'Risk: {l}.')}
def decision_agent(s):
    r=RiskAssessment.model_validate(s['risk']); e=EvidenceAssessment.model_validate(s['evidence']); c=min(e.confidence,.85); d=DecisionProposal(priority=r.level,recommendation='Escalate for human review and verify road conditions before operational action.',confidence=c); return {'decision':d.model_dump(),'trace':_t(s,f'Decision: priority={r.level}, confidence={c:.2f}.')}
def critic_agent(s):
    e=EvidenceAssessment.model_validate(s['evidence']); rv=s.get('revision_count',0); q=CriticReview(status='REVISE',reason='Road condition is unverified; request another evidence cycle.') if not e.evidence_complete and rv<1 else CriticReview(status='PASS',reason='Uncertainty is explicit and can proceed to safety review.'); return {'critic':q.model_dump(),'trace':_t(s,f'Critic: {q.status} — {q.reason}')}
def revision_agent(s):
    c=s.get('revision_count',0)+1; return {'revision_count':c,'trace':_t(s,f'Revision: cycle {c}; unresolved evidence remains explicit.')}
def safety_agent(s):
    d=DecisionProposal.model_validate(s['decision']); e=EvidenceAssessment.model_validate(s['evidence']); q=SafetyReview(status='HUMAN_REVIEW_REQUIRED',reason='Critical evidence is incomplete or confidence is below threshold.') if not e.evidence_complete or d.confidence<.70 else SafetyReview(status='APPROVED_WITH_LIMITATIONS',reason='Recommendation may be presented to a human operator; no autonomous action.'); return {'safety':q.model_dump(),'trace':_t(s,f'Safety: {q.status}.')}
def reporter_agent(s):
    i=Incident.model_validate(s['incident']); d=DecisionProposal.model_validate(s['decision']); q=SafetyReview.model_validate(s['safety']); x=f'Incident {i.incident_id} — {i.location}\nPriority: {d.priority}\nRecommendation: {d.recommendation}\nConfidence: {d.confidence:.2f}\nSafety status: {q.status}\nLimitation: {q.reason}\nPrinciple: AI recommends. AI explains. Humans decide.'; return {'final_report':x,'trace':_t(s,'Reporter: explainable response generated.')}
