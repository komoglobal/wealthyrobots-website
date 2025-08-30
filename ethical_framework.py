"""
ETHICAL FRAMEWORK
=================
Comprehensive ethical decision-making and value alignment system for AGI.
Ensures beneficial intelligence through principled decision-making and moral reasoning.
"""

import time
import json
import threading
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable
from enum import Enum
import sys

class EthicalPrinciple(Enum):
    """Core ethical principles"""
    BENEFICENCE = "beneficence"           # Do good
    NON_MALEFICENCE = "non_maleficence"   # Do no harm
    AUTONOMY = "autonomy"                 # Respect autonomy
    JUSTICE = "justice"                   # Fairness and equity
    TRANSPARENCY = "transparency"         # Openness and accountability
    PRIVACY = "privacy"                   # Respect privacy
    SUSTAINABILITY = "sustainability"     # Long-term thinking
    HUMAN_CENTRIC = "human_centric"       # Human well-being focus

class EthicalSeverity(Enum):
    """Ethical concern severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EthicalDecision(Enum):
    """Ethical decision outcomes"""
    APPROVED = "approved"
    CONDITIONAL = "conditional"
    DENIED = "denied"
    REQUIRES_REVIEW = "requires_review"

class EthicalFramework:
    """Comprehensive ethical framework for AGI decision-making"""

    def __init__(self):
        self.ethical_principles = {}
        self.decision_history = []
        self.ethical_dilemmas = []
        self.value_alignment_metrics = {}
        self.bias_detection_results = []
        self.transparency_log = []

        self.ethical_lock = threading.Lock()
        self.monitoring_active = False
        self.ethical_compliance_score = 100

        self._initialize_ethical_framework()
        self._start_ethical_monitoring()

    def _initialize_ethical_framework(self):
        """Initialize ethical framework components"""
        print("⚖️  ETHICAL FRAMEWORK INITIALIZING...")
        print("=" * 50)

        # Initialize core ethical principles with weights
        self.ethical_principles = {
            EthicalPrinciple.BENEFICENCE: {
                "weight": 0.25,
                "description": "Maximize overall benefit and well-being",
                "guidelines": ["Promote positive outcomes", "Prevent harm", "Enhance quality of life"]
            },
            EthicalPrinciple.NON_MALEFICENCE: {
                "weight": 0.20,
                "description": "Avoid causing harm or damage",
                "guidelines": ["Minimize risk", "Prevent negative consequences", "Ensure safety"]
            },
            EthicalPrinciple.AUTONOMY: {
                "weight": 0.15,
                "description": "Respect individual autonomy and choice",
                "guidelines": ["Honor personal agency", "Avoid manipulation", "Enable informed decisions"]
            },
            EthicalPrinciple.JUSTICE: {
                "weight": 0.15,
                "description": "Ensure fairness and equitable treatment",
                "guidelines": ["Fair resource distribution", "Equal opportunity", "Avoid discrimination"]
            },
            EthicalPrinciple.TRANSPARENCY: {
                "weight": 0.10,
                "description": "Maintain openness and accountability",
                "guidelines": ["Clear decision processes", "Explainable actions", "Open communication"]
            },
            EthicalPrinciple.PRIVACY: {
                "weight": 0.08,
                "description": "Protect personal privacy and data",
                "guidelines": ["Minimize data collection", "Secure data handling", "Respect confidentiality"]
            },
            EthicalPrinciple.SUSTAINABILITY: {
                "weight": 0.05,
                "description": "Consider long-term consequences",
                "guidelines": ["Environmental impact", "Resource conservation", "Future generations"]
            },
            EthicalPrinciple.HUMAN_CENTRIC: {
                "weight": 0.02,
                "description": "Prioritize human well-being and flourishing",
                "guidelines": ["Human needs first", "Enhance human potential", "Support human development"]
            }
        }

        # Initialize ethical decision-making components
        self.ethical_analyzers = {
            "impact_assessor": self._assess_ethical_impact,
            "bias_detector": self._detect_bias,
            "value_aligner": self._check_value_alignment,
            "dilemma_resolver": self._resolve_ethical_dilemma
        }

        # Initialize transparency and accountability systems
        self.transparency_system = {
            "decision_logger": self._log_ethical_decision,
            "reasoning_recorder": self._record_ethical_reasoning,
            "impact_tracker": self._track_ethical_impact,
            "compliance_monitor": self._monitor_ethical_compliance
        }

        print("✅ Ethical principles established")
        print("✅ Decision-making framework configured")
        print("✅ Transparency systems activated")

    def _start_ethical_monitoring(self):
        """Start ethical monitoring threads"""
        print("\n👁️  STARTING ETHICAL MONITORING...")
        print("=" * 40)

        # Start monitoring threads
        self.ethical_assessment_thread = threading.Thread(target=self._ethical_assessment_loop)
        self.ethical_assessment_thread.daemon = True
        self.ethical_assessment_thread.start()

        self.bias_monitoring_thread = threading.Thread(target=self._bias_monitoring_loop)
        self.bias_monitoring_thread.daemon = True
        self.bias_monitoring_thread.start()

        self.compliance_monitoring_thread = threading.Thread(target=self._compliance_monitoring_loop)
        self.compliance_monitoring_thread.daemon = True
        self.compliance_monitoring_thread.start()

        print("✅ Ethical assessment thread started")
        print("✅ Bias monitoring thread started")
        print("✅ Compliance monitoring thread started")

        self.monitoring_active = True

    def _ethical_assessment_loop(self):
        """Continuous ethical assessment"""
        while self.monitoring_active:
            try:
                time.sleep(60)  # Assess every minute

                self._perform_ethical_self_assessment()
                self._evaluate_decision_ethics()
                self._monitor_ethical_trends()

            except Exception as e:
                print(f"⚠️  Ethical assessment error: {e}")
                time.sleep(120)

    def _bias_monitoring_loop(self):
        """Continuous bias monitoring"""
        while self.monitoring_active:
            try:
                time.sleep(300)  # Monitor every 5 minutes

                self._scan_for_biases()
                self._assess_fairness()
                self._monitor_discrimination()

            except Exception as e:
                print(f"⚠️  Bias monitoring error: {e}")
                time.sleep(180)

    def _predict_immediate_effects(self, decision_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict immediate effects of decision"""
        try:
            effects = [{"type": "efficiency", "description": "Immediate efficiency improvement", "probability": 80}]
            return effects
        except Exception:
            return []

    def _predict_short_term_effects(self, decision_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict short-term effects of decision"""
        try:
            effects = [{"type": "adaptation", "description": "Short-term adaptation period", "probability": 90}]
            return effects
        except Exception:
            return []

    def _predict_long_term_effects(self, decision_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Predict long-term effects of decision"""
        try:
            effects = [{"type": "growth", "description": "Long-term growth potential", "probability": 70}]
            return effects
        except Exception:
            return []

    def _evaluate_stakeholder_impact(self, decision_context: Dict[str, Any], stakeholder: str) -> Dict[str, Any]:
        """Evaluate impact on specific stakeholder"""
        try:
            return {"sentiment": "neutral", "impact_level": "moderate"}
        except Exception:
            return {"sentiment": "unknown", "impact_level": "unknown"}

    def _assess_sustainability_impact(self, decision_context: Dict[str, Any]) -> str:
        """Evaluate sustainability impact"""
        try:
            return "moderate"
        except Exception:
            return "unknown"

    def _assess_scalability(self, decision_context: Dict[str, Any]) -> str:
        """Assess scalability"""
        try:
            return "good"
        except Exception:
            return "unknown"

    def _analyze_future_implications(self, decision_context: Dict[str, Any]) -> List[str]:
        """Analyze future implications"""
        try:
            return ["potential_growth", "technological_advancement"]
        except Exception:
            return []

    def _resolve_ethical_dilemma(self, dilemma_context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve ethical dilemma"""
        try:
            return {"resolution": "balanced_approach", "reasoning": "Balanced approach recommended"}
        except Exception:
            return {"resolution": "requires_review", "reasoning": "Dilemma resolution failed"}

    def _analyze_dilemma(self, dilemma_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze ethical dilemma"""
        try:
            return {"complexity": "medium", "stakeholders": 3, "urgency": dilemma_context.get("urgency", "medium")}
        except Exception:
            return {"complexity": "unknown"}

    def _evaluate_dilemma_options(self, dilemma_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate dilemma options"""
        try:
            return {"best_option": "balanced_approach", "confidence": 75}
        except Exception:
            return {"best_option": "unknown"}

    def _apply_ethical_reasoning(self, dilemma_analysis: Dict, option_evaluation: Dict) -> Dict[str, Any]:
        """Apply ethical reasoning"""
        try:
            return {"resolution": "balanced_approach", "reasoning": "Applying ethical principles for balanced solution", "confidence": 80}
        except Exception:
            return {"resolution": "requires_review"}

    def _compliance_monitoring_loop(self):
        """Continuous ethical compliance monitoring"""
        while self.monitoring_active:
            try:
                time.sleep(180)  # Monitor every 3 minutes

                self._check_principle_compliance()
                self._assess_overall_alignment()
                self._generate_ethical_report()

            except Exception as e:
                print(f"⚠️  Compliance monitoring error: {e}")
                time.sleep(240)

    def evaluate_decision_ethics(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the ethics of a decision or action"""
        with self.ethical_lock:
            try:
                # Assess ethical impact
                impact_assessment = self._assess_ethical_impact(decision_context)

                # Check value alignment
                alignment_check = self._check_value_alignment(decision_context)

                # Detect potential biases
                bias_analysis = self._detect_bias(decision_context)

                # Evaluate against principles
                principle_evaluation = self._evaluate_against_principles(decision_context)

                # Make ethical decision
                ethical_decision = self._make_ethical_decision(
                    impact_assessment,
                    alignment_check,
                    bias_analysis,
                    principle_evaluation
                )

                # Log decision
                decision_record = {
                    "timestamp": datetime.now().isoformat(),
                    "decision_context": decision_context,
                    "impact_assessment": impact_assessment,
                    "alignment_check": alignment_check,
                    "bias_analysis": bias_analysis,
                    "principle_evaluation": principle_evaluation,
                    "ethical_decision": ethical_decision,
                    "reasoning": self._generate_ethical_reasoning(decision_context, ethical_decision)
                }

                self.decision_history.append(decision_record)
                self._log_ethical_decision(decision_record)

                # Maintain history size
                if len(self.decision_history) > 1000:
                    self.decision_history = self.decision_history[-500:]

                return ethical_decision

            except Exception as e:
                print(f"⚠️  Ethical evaluation error: {e}")
                return {
                    "decision": EthicalDecision.REQUIRES_REVIEW.value,
                    "reasoning": f"Ethical evaluation failed: {str(e)}",
                    "severity": EthicalSeverity.CRITICAL.value,
                    "requires_human_review": True
                }

    def _assess_ethical_impact(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the ethical impact of a decision"""
        try:
            # Analyze potential consequences
            consequences = self._analyze_consequences(decision_context)

            # Evaluate stakeholder impact
            stakeholder_impact = self._evaluate_stakeholder_impact(decision_context)

            # Assess long-term effects
            long_term_effects = self._assess_long_term_effects(decision_context)

            # Calculate overall impact score
            impact_score = self._calculate_impact_score(consequences, stakeholder_impact, long_term_effects)

            return {
                "consequences": consequences,
                "stakeholder_impact": stakeholder_impact,
                "long_term_effects": long_term_effects,
                "overall_impact_score": impact_score,
                "impact_assessment": self._interpret_impact_score(impact_score)
            }

        except Exception as e:
            print(f"⚠️  Impact assessment error: {e}")
            return {"error": str(e), "overall_impact_score": 50}

    def _check_value_alignment(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Check alignment with core values"""
        try:
            alignment_scores = {}

            for principle, config in self.ethical_principles.items():
                alignment_score = self._calculate_principle_alignment(decision_context, principle, config)
                alignment_scores[principle.value] = alignment_score

            # Calculate overall alignment
            overall_alignment = sum(
                score * self.ethical_principles[EthicalPrinciple(principle)].get("weight", 0.1)
                for principle, score in alignment_scores.items()
            ) * 100

            return {
                "principle_alignment_scores": alignment_scores,
                "overall_alignment": round(overall_alignment, 1),
                "alignment_interpretation": self._interpret_alignment_score(overall_alignment),
                "misaligned_principles": [p for p, s in alignment_scores.items() if s < 60]
            }

        except Exception as e:
            print(f"⚠️  Value alignment check error: {e}")
            return {"error": str(e), "overall_alignment": 50}

    def _detect_bias(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Detect potential biases in decision-making"""
        try:
            bias_indicators = []

            # Check for confirmation bias
            confirmation_bias = self._check_confirmation_bias(decision_context)
            if confirmation_bias["detected"]:
                bias_indicators.append({
                    "type": "confirmation_bias",
                    "severity": confirmation_bias["severity"],
                    "description": confirmation_bias["description"]
                })

            # Check for availability bias
            availability_bias = self._check_availability_bias(decision_context)
            if availability_bias["detected"]:
                bias_indicators.append({
                    "type": "availability_bias",
                    "severity": availability_bias["severity"],
                    "description": availability_bias["description"]
                })

            # Check for anchoring bias
            anchoring_bias = self._check_anchoring_bias(decision_context)
            if anchoring_bias["detected"]:
                bias_indicators.append({
                    "type": "anchoring_bias",
                    "severity": anchoring_bias["severity"],
                    "description": anchoring_bias["description"]
                })

            return {
                "bias_indicators": bias_indicators,
                "bias_detected": len(bias_indicators) > 0,
                "bias_severity": max([b.get("severity", "low") for b in bias_indicators], default="low")
            }

        except Exception as e:
            print(f"⚠️  Bias detection error: {e}")
            return {"bias_detected": False, "error": str(e)}

    def _evaluate_against_principles(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate decision against ethical principles"""
        try:
            principle_scores = {}

            for principle, config in self.ethical_principles.items():
                # Evaluate how well decision aligns with principle
                principle_score = self._evaluate_principle_compliance(decision_context, principle)
                principle_scores[principle.value] = principle_score

            # Identify violated principles
            violated_principles = [p for p, s in principle_scores.items() if s < 50]

            return {
                "principle_scores": principle_scores,
                "violated_principles": violated_principles,
                "compliance_level": "good" if len(violated_principles) == 0 else "poor",
                "recommendations": self._generate_principle_recommendations(violated_principles)
            }

        except Exception as e:
            print(f"⚠️  Principle evaluation error: {e}")
            return {"error": str(e), "compliance_level": "unknown"}

    def _make_ethical_decision(self, impact_assessment: Dict, alignment_check: Dict,
                              bias_analysis: Dict, principle_evaluation: Dict) -> Dict[str, Any]:
        """Make final ethical decision"""
        try:
            # Combine all assessments
            decision_factors = {
                "impact_score": impact_assessment.get("overall_impact_score", 50),
                "alignment_score": alignment_check.get("overall_alignment", 50),
                "bias_detected": bias_analysis.get("bias_detected", False),
                "principle_violations": len(principle_evaluation.get("violated_principles", []))
            }

            # Decision logic
            if decision_factors["impact_score"] < 30 or decision_factors["bias_detected"] or decision_factors["principle_violations"] > 2:
                decision = EthicalDecision.DENIED
                reasoning = "Decision violates multiple ethical principles or poses significant risk"
            elif decision_factors["impact_score"] < 50 or decision_factors["alignment_score"] < 60 or decision_factors["principle_violations"] > 0:
                decision = EthicalDecision.CONDITIONAL
                reasoning = "Decision requires conditions or modifications to be ethically acceptable"
            elif decision_factors["impact_score"] >= 70 and decision_factors["alignment_score"] >= 80 and not decision_factors["bias_detected"]:
                decision = EthicalDecision.APPROVED
                reasoning = "Decision aligns well with ethical principles and poses minimal risk"
            else:
                decision = EthicalDecision.REQUIRES_REVIEW
                reasoning = "Decision requires additional ethical review"

            return {
                "decision": decision.value,
                "reasoning": reasoning,
                "confidence": self._calculate_decision_confidence(decision_factors),
                "conditions": self._generate_decision_conditions(decision) if decision == EthicalDecision.CONDITIONAL else [],
                "requires_human_review": decision in [EthicalDecision.REQUIRES_REVIEW, EthicalDecision.DENIED]
            }

        except Exception as e:
            print(f"⚠️  Ethical decision making error: {e}")
            return {
                "decision": EthicalDecision.REQUIRES_REVIEW.value,
                "reasoning": f"Decision process failed: {str(e)}",
                "requires_human_review": True
            }

    def resolve_ethical_dilemma(self, dilemma_context: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve an ethical dilemma"""
        with self.ethical_lock:
            try:
                # Analyze dilemma
                dilemma_analysis = self._analyze_dilemma(dilemma_context)

                # Evaluate options
                option_evaluation = self._evaluate_dilemma_options(dilemma_context)

                # Apply ethical reasoning
                resolution = self._apply_ethical_reasoning(dilemma_analysis, option_evaluation)

                # Record dilemma and resolution
                dilemma_record = {
                    "timestamp": datetime.now().isoformat(),
                    "dilemma_context": dilemma_context,
                    "analysis": dilemma_analysis,
                    "option_evaluation": option_evaluation,
                    "resolution": resolution
                }

                self.ethical_dilemmas.append(dilemma_record)

                # Maintain history size
                if len(self.ethical_dilemmas) > 200:
                    self.ethical_dilemmas = self.ethical_dilemmas[-100:]

                return resolution

            except Exception as e:
                print(f"⚠️  Ethical dilemma resolution error: {e}")
                return {
                    "resolution": "requires_human_intervention",
                    "reasoning": f"Dilemma resolution failed: {str(e)}",
                    "requires_human_review": True
                }

    def _analyze_consequences(self, decision_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze potential consequences of decision"""
        try:
            consequences = []

            # Analyze immediate consequences
            immediate_effects = self._predict_immediate_effects(decision_context)
            consequences.extend(immediate_effects)

            # Analyze short-term consequences
            short_term_effects = self._predict_short_term_effects(decision_context)
            consequences.extend(short_term_effects)

            # Analyze long-term consequences
            long_term_effects = self._predict_long_term_effects(decision_context)
            consequences.extend(long_term_effects)

            return consequences

        except Exception:
            return [{"type": "unknown", "description": "Consequence analysis failed", "probability": 50}]

    def _evaluate_stakeholder_impact(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate impact on stakeholders"""
        try:
            stakeholders = ["users", "developers", "organization", "society", "environment"]

            stakeholder_impacts = {}
            for stakeholder in stakeholders:
                impact = self._assess_stakeholder_impact(decision_context, stakeholder)
                stakeholder_impacts[stakeholder] = impact

            # Calculate overall stakeholder impact
            positive_impacts = sum(1 for impact in stakeholder_impacts.values() if impact.get("sentiment", "neutral") == "positive")
            negative_impacts = sum(1 for impact in stakeholder_impacts.values() if impact.get("sentiment", "neutral") == "negative")

            overall_sentiment = "positive" if positive_impacts > negative_impacts else "negative" if negative_impacts > positive_impacts else "neutral"

            return {
                "stakeholder_impacts": stakeholder_impacts,
                "overall_sentiment": overall_sentiment,
                "positive_impacts": positive_impacts,
                "negative_impacts": negative_impacts
            }

        except Exception:
            return {"stakeholder_impacts": {}, "overall_sentiment": "unknown"}

    def _assess_long_term_effects(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """Assess long-term effects"""
        try:
            # Consider sustainability
            sustainability_impact = self._evaluate_sustainability_impact(decision_context)

            # Consider scalability
            scalability_assessment = self._assess_scalability(decision_context)

            # Consider future implications
            future_implications = self._analyze_future_implications(decision_context)

            return {
                "sustainability_impact": sustainability_impact,
                "scalability_assessment": scalability_assessment,
                "future_implications": future_implications,
                "long_term_risk_level": self._calculate_long_term_risk(sustainability_impact, scalability_assessment, future_implications)
            }

        except Exception:
            return {"long_term_risk_level": "unknown"}

    def _calculate_impact_score(self, consequences: List, stakeholder_impact: Dict, long_term_effects: Dict) -> float:
        """Calculate overall impact score"""
        try:
            # Score consequences (0-100)
            consequence_score = 50  # Neutral baseline
            if consequences:
                positive_consequences = sum(1 for c in consequences if c.get("sentiment") == "positive")
                consequence_score = (positive_consequences / len(consequences)) * 100

            # Score stakeholder impact (0-100)
            stakeholder_score = 50  # Neutral baseline
            if stakeholder_impact.get("overall_sentiment") == "positive":
                stakeholder_score = 80
            elif stakeholder_impact.get("overall_sentiment") == "negative":
                stakeholder_score = 20

            # Score long-term effects (0-100)
            long_term_score = 100 - (long_term_effects.get("long_term_risk_level", "medium") == "high" and 40 or
                                   long_term_effects.get("long_term_risk_level", "medium") == "low" and 10 or 20)

            # Weighted average
            overall_score = (consequence_score * 0.4 + stakeholder_score * 0.4 + long_term_score * 0.2)

            return round(overall_score, 1)

        except Exception:
            return 50.0

    def _interpret_impact_score(self, score: float) -> str:
        """Interpret impact score"""
        if score >= 80:
            return "highly_positive"
        elif score >= 60:
            return "moderately_positive"
        elif score >= 40:
            return "neutral"
        elif score >= 20:
            return "moderately_negative"
        else:
            return "highly_negative"

    def _calculate_principle_alignment(self, decision_context: Dict, principle: EthicalPrinciple, config: Dict) -> float:
        """Calculate alignment with specific ethical principle"""
        try:
            # Simple alignment calculation based on decision context
            alignment_indicators = config.get("guidelines", [])

            alignment_score = 50  # Neutral baseline

            # Check how well decision aligns with principle guidelines
            for guideline in alignment_indicators:
                if self._check_guideline_alignment(decision_context, guideline):
                    alignment_score += 10
                else:
                    alignment_score -= 5

            return max(0, min(100, alignment_score))

        except Exception:
            return 50.0

    def _check_guideline_alignment(self, decision_context: Dict, guideline: str) -> bool:
        """Check if decision aligns with specific guideline"""
        try:
            # Simple keyword-based alignment check
            decision_text = str(decision_context.get("description", "")).lower()
            guideline_keywords = guideline.lower().split()

            alignment_score = sum(1 for keyword in guideline_keywords if keyword in decision_text)
            return alignment_score > 0

        except Exception:
            return False

    def _interpret_alignment_score(self, score: float) -> str:
        """Interpret alignment score"""
        if score >= 80:
            return "excellent_alignment"
        elif score >= 60:
            return "good_alignment"
        elif score >= 40:
            return "moderate_alignment"
        else:
            return "poor_alignment"

    def _check_confirmation_bias(self, decision_context: Dict) -> Dict[str, Any]:
        """Check for confirmation bias"""
        try:
            # Simple bias detection
            decision_text = str(decision_context.get("description", "")).lower()

            bias_indicators = ["always", "never", "obviously", "clearly", "definitely"]
            bias_detected = any(indicator in decision_text for indicator in bias_indicators)

            return {
                "detected": bias_detected,
                "severity": "medium" if bias_detected else "low",
                "description": "Confirmation bias detected in decision reasoning" if bias_detected else "No confirmation bias detected"
            }

        except Exception:
            return {"detected": False, "severity": "low", "description": "Bias check failed"}

    def _check_availability_bias(self, decision_context: Dict) -> Dict[str, Any]:
        """Check for availability bias"""
        try:
            # Check if decision is based on recent or memorable events
            decision_text = str(decision_context.get("description", "")).lower()

            bias_indicators = ["recently", "lately", "just happened", "fresh in mind"]
            bias_detected = any(indicator in decision_text for indicator in bias_indicators)

            return {
                "detected": bias_detected,
                "severity": "low" if bias_detected else "low",
                "description": "Availability bias may be influencing decision" if bias_detected else "No availability bias detected"
            }

        except Exception:
            return {"detected": False, "severity": "low", "description": "Bias check failed"}

    def _check_anchoring_bias(self, decision_context: Dict) -> Dict[str, Any]:
        """Check for anchoring bias"""
        try:
            # Check if decision is anchored to initial information
            decision_text = str(decision_context.get("description", "")).lower()

            bias_indicators = ["initially", "originally", "first", "starting point"]
            bias_detected = any(indicator in decision_text for indicator in bias_indicators)

            return {
                "detected": bias_detected,
                "severity": "low" if bias_detected else "low",
                "description": "Anchoring bias may be present" if bias_detected else "No anchoring bias detected"
            }

        except Exception:
            return {"detected": False, "severity": "low", "description": "Bias check failed"}

    def _evaluate_principle_compliance(self, decision_context: Dict, principle: EthicalPrinciple) -> float:
        """Evaluate compliance with specific ethical principle"""
        try:
            # Get principle configuration
            config = self.ethical_principles.get(principle, {})
            guidelines = config.get("guidelines", [])

            compliance_score = 100  # Start with perfect compliance

            # Check each guideline
            for guideline in guidelines:
                if not self._check_guideline_compliance(decision_context, guideline):
                    compliance_score -= 20  # Reduce score for non-compliance

            return max(0, compliance_score)

        except Exception:
            return 50.0

    def _check_guideline_compliance(self, decision_context: Dict, guideline: str) -> bool:
        """Check if decision complies with specific guideline"""
        try:
            # Simple compliance check
            decision_text = str(decision_context.get("description", "")).lower()

            # This would be more sophisticated in a real implementation
            return len(decision_text) > 10  # Placeholder logic

        except Exception:
            return False

    def _generate_principle_recommendations(self, violated_principles: List[str]) -> List[str]:
        """Generate recommendations for violated principles"""
        try:
            recommendations = []

            for principle in violated_principles:
                if principle == "beneficence":
                    recommendations.append("Consider alternative approaches that maximize overall benefit")
                elif principle == "non_maleficence":
                    recommendations.append("Implement additional safeguards to prevent potential harm")
                elif principle == "autonomy":
                    recommendations.append("Ensure decision respects individual autonomy and choice")
                elif principle == "justice":
                    recommendations.append("Review decision for fairness and equitable treatment")
                elif principle == "transparency":
                    recommendations.append("Increase transparency in decision-making process")
                elif principle == "privacy":
                    recommendations.append("Enhance privacy protections and data handling")
                elif principle == "sustainability":
                    recommendations.append("Consider long-term environmental and social impacts")
                elif principle == "human_centric":
                    recommendations.append("Prioritize human well-being and needs")

            return recommendations

        except Exception:
            return ["Review decision against ethical principles"]

    def _calculate_decision_confidence(self, decision_factors: Dict) -> float:
        """Calculate confidence in ethical decision"""
        try:
            # Base confidence
            confidence = 70

            # Adjust based on factors
            if decision_factors.get("impact_score", 50) > 70:
                confidence += 15
            elif decision_factors.get("impact_score", 50) < 30:
                confidence -= 20

            if decision_factors.get("alignment_score", 50) > 80:
                confidence += 10
            elif decision_factors.get("alignment_score", 50) < 60:
                confidence -= 15

            if decision_factors.get("bias_detected", False):
                confidence -= 25

            if decision_factors.get("principle_violations", 0) > 0:
                confidence -= decision_factors["principle_violations"] * 10

            return max(0, min(100, confidence))

        except Exception:
            return 50.0

    def _generate_decision_conditions(self, decision: EthicalDecision) -> List[str]:
        """Generate conditions for conditional approval"""
        try:
            conditions = []

            if decision == EthicalDecision.CONDITIONAL:
                conditions = [
                    "Implement additional monitoring and oversight",
                    "Conduct regular ethical impact assessments",
                    "Maintain detailed decision documentation",
                    "Establish clear escalation procedures for issues"
                ]

            return conditions

        except Exception:
            return ["Additional ethical review required"]

    def _generate_ethical_reasoning(self, decision_context: Dict, ethical_decision: Dict) -> str:
        """Generate detailed ethical reasoning"""
        try:
            reasoning_parts = [
                f"Decision: {ethical_decision.get('decision', 'unknown')}",
                f"Reasoning: {ethical_decision.get('reasoning', 'No reasoning provided')}",
                f"Confidence: {ethical_decision.get('confidence', 0)}%",
                f"Decision Context: {decision_context.get('description', 'No context provided')}"
            ]

            return " | ".join(reasoning_parts)

        except Exception:
            return "Ethical reasoning generation failed"

    def _log_ethical_decision(self, decision_record: Dict):
        """Log ethical decision for transparency"""
        try:
            self.transparency_log.append({
                "timestamp": decision_record["timestamp"],
                "decision": decision_record["ethical_decision"]["decision"],
                "reasoning": decision_record["ethical_decision"]["reasoning"],
                "confidence": decision_record["ethical_decision"]["confidence"]
            })

            # Maintain log size
            if len(self.transparency_log) > 500:
                self.transparency_log = self.transparency_log[-200:]

        except Exception as e:
            print(f"⚠️  Decision logging error: {e}")

    def _record_ethical_reasoning(self, reasoning: str):
        """Record ethical reasoning process"""
        try:
            self.transparency_log.append({
                "timestamp": datetime.now().isoformat(),
                "type": "reasoning_record",
                "content": reasoning
            })

        except Exception as e:
            print(f"⚠️  Reasoning recording error: {e}")

    def _track_ethical_impact(self, impact_data: Dict):
        """Track ethical impact of decisions"""
        try:
            self.transparency_log.append({
                "timestamp": datetime.now().isoformat(),
                "type": "impact_tracking",
                "impact_data": impact_data
            })

        except Exception as e:
            print(f"⚠️  Impact tracking error: {e}")

    def _monitor_ethical_compliance(self):
        """Monitor overall ethical compliance"""
        try:
            if len(self.decision_history) < 5:
                return

            recent_decisions = self.decision_history[-20:]

            # Calculate compliance metrics
            approved_decisions = len([d for d in recent_decisions if d["ethical_decision"]["decision"] == "approved"])
            compliance_rate = (approved_decisions / len(recent_decisions)) * 100

            self.ethical_compliance_score = compliance_rate

        except Exception as e:
            print(f"⚠️  Compliance monitoring error: {e}")

    def _perform_ethical_self_assessment(self):
        """Perform ethical self-assessment"""
        try:
            assessment = {
                "timestamp": datetime.now().isoformat(),
                "compliance_score": self.ethical_compliance_score,
                "recent_decisions_count": len([d for d in self.decision_history if (datetime.now() - datetime.fromisoformat(d["timestamp"])).seconds < 3600]),
                "ethical_dilemmas_count": len(self.ethical_dilemmas),
                "bias_incidents_count": len([b for b in self.bias_detection_results if b.get("detected", False)])
            }

            # Store assessment
            self.value_alignment_metrics["latest_assessment"] = assessment

        except Exception as e:
            print(f"⚠️  Ethical self-assessment error: {e}")

    def _evaluate_decision_ethics(self):
        """Evaluate ethics of recent decisions"""
        try:
            if len(self.decision_history) < 10:
                return

            recent_decisions = self.decision_history[-10:]

            # Analyze decision patterns
            decision_patterns = {
                "approved": len([d for d in recent_decisions if d["ethical_decision"]["decision"] == "approved"]),
                "conditional": len([d for d in recent_decisions if d["ethical_decision"]["decision"] == "conditional"]),
                "denied": len([d for d in recent_decisions if d["ethical_decision"]["decision"] == "denied"]),
                "requires_review": len([d for d in recent_decisions if d["ethical_decision"]["decision"] == "requires_review"])
            }

            # Check for concerning patterns
            if decision_patterns["denied"] > 5:
                print(f"⚠️  HIGH NUMBER OF DENIED DECISIONS: {decision_patterns['denied']} in last 10 decisions")
            elif decision_patterns["requires_review"] > 7:
                print(f"⚠️  HIGH NUMBER OF DECISIONS REQUIRING REVIEW: {decision_patterns['requires_review']} in last 10 decisions")

        except Exception as e:
            print(f"⚠️  Decision ethics evaluation error: {e}")

    def _monitor_ethical_trends(self):
        """Monitor ethical decision trends"""
        try:
            if len(self.decision_history) < 20:
                return

            # Analyze trends in ethical compliance
            recent_compliance = [d["ethical_decision"].get("confidence", 50) for d in self.decision_history[-20:]]
            compliance_trend = sum(recent_compliance) / len(recent_compliance)

            if compliance_trend < 60:
                print(f"⚠️  ETHICAL COMPLIANCE TREND DECLINING: {compliance_trend:.1f}% average confidence")
            elif compliance_trend > 85:
                print(f"✅ ETHICAL COMPLIANCE EXCELLENT: {compliance_trend:.1f}% average confidence")

        except Exception as e:
            print(f"⚠️  Ethical trend monitoring error: {e}")

    def _scan_for_biases(self):
        """Scan for biases in decision-making"""
        try:
            if len(self.decision_history) < 10:
                return

            recent_decisions = self.decision_history[-10:]

            bias_scan = {
                "confirmation_bias_indicators": 0,
                "availability_bias_indicators": 0,
                "anchoring_bias_indicators": 0,
                "scanned_decisions": len(recent_decisions)
            }

            for decision in recent_decisions:
                context = decision.get("decision_context", {})
                bias_analysis = self._detect_bias(context)

                if bias_analysis.get("bias_detected", False):
                    for bias in bias_analysis.get("bias_indicators", []):
                        bias_type = bias.get("type", "")
                        if "confirmation" in bias_type:
                            bias_scan["confirmation_bias_indicators"] += 1
                        elif "availability" in bias_type:
                            bias_scan["availability_bias_indicators"] += 1
                        elif "anchoring" in bias_type:
                            bias_scan["anchoring_bias_indicators"] += 1

            # Store bias scan results
            self.bias_detection_results.append({
                "timestamp": datetime.now().isoformat(),
                "scan_results": bias_scan
            })

            # Alert on high bias levels
            total_biases = sum(bias_scan.values()) - bias_scan["scanned_decisions"]
            if total_biases > 3:
                print(f"⚠️  HIGH BIAS LEVELS DETECTED: {total_biases} bias indicators in recent decisions")

        except Exception as e:
            print(f"⚠️  Bias scanning error: {e}")

    def _assess_fairness(self):
        """Assess fairness in decision-making"""
        try:
            if len(self.decision_history) < 15:
                return

            recent_decisions = self.decision_history[-15:]

            # Analyze decision distribution
            decision_types = {}
            for decision in recent_decisions:
                decision_type = decision["ethical_decision"]["decision"]
                decision_types[decision_type] = decision_types.get(decision_type, 0) + 1

            # Check for fairness concerns
            total_decisions = len(recent_decisions)
            denied_percentage = (decision_types.get("denied", 0) / total_decisions) * 100

            if denied_percentage > 60:
                print(f"⚠️  FAIRNESS CONCERN: {denied_percentage:.1f}% of recent decisions denied")
            elif denied_percentage < 10:
                print(f"✅ DECISION FAIRNESS GOOD: Only {denied_percentage:.1f}% of decisions denied")

        except Exception as e:
            print(f"⚠️  Fairness assessment error: {e}")

    def _monitor_discrimination(self):
        """Monitor for discrimination in decisions"""
        try:
            # This would be more sophisticated in a real implementation
            # For now, we'll do a simple pattern check
            if len(self.decision_history) < 20:
                return

            recent_decisions = self.decision_history[-20:]

            # Check for patterns that might indicate discrimination
            discrimination_indicators = 0

            for decision in recent_decisions:
                context = str(decision.get("decision_context", {}).get("description", "")).lower()
                if any(word in context for word in ["discriminate", "unfair", "bias", "prejudice"]):
                    discrimination_indicators += 1

            if discrimination_indicators > 5:
                print(f"🚨 DISCRIMINATION CONCERN: {discrimination_indicators} potential discrimination indicators detected")

        except Exception as e:
            print(f"⚠️  Discrimination monitoring error: {e}")

    def _check_principle_compliance(self):
        """Check compliance with ethical principles"""
        try:
            if len(self.decision_history) < 10:
                return

            recent_decisions = self.decision_history[-10:]

            principle_compliance = {}

            for principle in self.ethical_principles.keys():
                principle_name = principle.value
                compliant_decisions = 0

                for decision in recent_decisions:
                    principle_scores = decision.get("principle_evaluation", {}).get("principle_scores", {})
                    if principle_scores.get(principle_name, 50) >= 70:
                        compliant_decisions += 1

                compliance_rate = (compliant_decisions / len(recent_decisions)) * 100
                principle_compliance[principle_name] = compliance_rate

                if compliance_rate < 50:
                    print(f"⚠️  LOW COMPLIANCE: {principle_name} compliance at {compliance_rate:.1f}%")

            self.value_alignment_metrics["principle_compliance"] = principle_compliance

        except Exception as e:
            print(f"⚠️  Principle compliance check error: {e}")

    def _assess_overall_alignment(self):
        """Assess overall value alignment"""
        try:
            if not self.value_alignment_metrics:
                return

            # Calculate overall alignment score
            compliance_scores = []
            if "principle_compliance" in self.value_alignment_metrics:
                compliance_scores = list(self.value_alignment_metrics["principle_compliance"].values())

            if compliance_scores:
                overall_alignment = sum(compliance_scores) / len(compliance_scores)

                if overall_alignment < 60:
                    print(f"⚠️  VALUE ALIGNMENT CONCERN: Overall alignment at {overall_alignment:.1f}%")
                elif overall_alignment > 85:
                    print(f"✅ EXCELLENT VALUE ALIGNMENT: {overall_alignment:.1f}% overall alignment")

                self.value_alignment_metrics["overall_alignment"] = overall_alignment

        except Exception as e:
            print(f"⚠️  Overall alignment assessment error: {e}")

    def _generate_ethical_report(self):
        """Generate comprehensive ethical report"""
        try:
            report = {
                "timestamp": datetime.now().isoformat(),
                "compliance_score": self.ethical_compliance_score,
                "value_alignment": self.value_alignment_metrics.get("overall_alignment", 0),
                "recent_decisions": len([d for d in self.decision_history if (datetime.now() - datetime.fromisoformat(d["timestamp"])).seconds < 3600]),
                "ethical_dilemmas_resolved": len(self.ethical_dilemmas),
                "bias_incidents": len([b for b in self.bias_detection_results if b.get("scan_results", {}).get("confirmation_bias_indicators", 0) > 0])
            }

            # Store report
            self.value_alignment_metrics["latest_report"] = report

            # Print summary
            print(f"📋 ETHICAL REPORT: Compliance {report['compliance_score']:.1f}%, Alignment {report['value_alignment']:.1f}%")

        except Exception as e:
            print(f"⚠️  Ethical report generation error: {e}")

    def get_ethical_status(self) -> Dict[str, Any]:
        """Get comprehensive ethical status"""
        try:
            with self.ethical_lock:
                return {
                    "ethical_compliance_score": self.ethical_compliance_score,
                    "value_alignment_metrics": self.value_alignment_metrics,
                    "recent_decisions_count": len([d for d in self.decision_history if (datetime.now() - datetime.fromisoformat(d["timestamp"])).seconds < 3600]),
                    "ethical_dilemmas_count": len(self.ethical_dilemmas),
                    "bias_detection_results": self.bias_detection_results[-5:],  # Last 5 bias scans
                    "transparency_log_entries": len(self.transparency_log),
                    "principle_compliance": self.value_alignment_metrics.get("principle_compliance", {}),
                    "monitoring_active": self.monitoring_active,
                    "last_update": datetime.now().isoformat()
                }

        except Exception as e:
            print(f"⚠️  Ethical status error: {e}")
            return {"error": str(e)}

    def get_ethical_report(self) -> Dict[str, Any]:
        """Generate comprehensive ethical report"""
        try:
            # Decision analysis
            decision_analysis = self._analyze_decision_patterns()

            # Principle compliance analysis
            principle_analysis = self._analyze_principle_compliance()

            # Bias analysis
            bias_analysis = self._analyze_bias_patterns()

            # Dilemma resolution analysis
            dilemma_analysis = self._analyze_dilemma_resolution()

            # Recommendations
            recommendations = self._generate_ethical_recommendations()

            return {
                "decision_analysis": decision_analysis,
                "principle_analysis": principle_analysis,
                "bias_analysis": bias_analysis,
                "dilemma_analysis": dilemma_analysis,
                "recommendations": recommendations,
                "generated_at": datetime.now().isoformat()
            }

        except Exception as e:
            print(f"⚠️  Ethical report generation error: {e}")
            return {"error": str(e)}

    def _analyze_decision_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in ethical decisions"""
        try:
            if len(self.decision_history) < 10:
                return {"status": "insufficient_data"}

            recent_decisions = self.decision_history[-50:]

            decision_counts = {}
            for decision in recent_decisions:
                decision_type = decision["ethical_decision"]["decision"]
                decision_counts[decision_type] = decision_counts.get(decision_type, 0) + 1

            total_decisions = len(recent_decisions)
            approval_rate = (decision_counts.get("approved", 0) / total_decisions) * 100

            return {
                "total_decisions": total_decisions,
                "decision_breakdown": decision_counts,
                "approval_rate": round(approval_rate, 1),
                "average_confidence": sum(d["ethical_decision"].get("confidence", 50) for d in recent_decisions) / total_decisions
            }

        except Exception:
            return {"status": "analysis_error"}

    def _analyze_principle_compliance(self) -> Dict[str, Any]:
        """Analyze compliance with ethical principles"""
        try:
            compliance_data = self.value_alignment_metrics.get("principle_compliance", {})

            if not compliance_data:
                return {"status": "no_compliance_data"}

            # Find strongest and weakest principles
            sorted_principles = sorted(compliance_data.items(), key=lambda x: x[1], reverse=True)

            return {
                "strongest_principle": sorted_principles[0][0] if sorted_principles else "unknown",
                "weakest_principle": sorted_principles[-1][0] if sorted_principles else "unknown",
                "average_compliance": sum(compliance_data.values()) / len(compliance_data),
                "principle_compliance_details": compliance_data
            }

        except Exception:
            return {"status": "compliance_analysis_error"}

    def _analyze_bias_patterns(self) -> Dict[str, Any]:
        """Analyze bias patterns"""
        try:
            if not self.bias_detection_results:
                return {"status": "no_bias_data"}

            recent_scans = self.bias_detection_results[-10:]

            total_bias_indicators = sum(
                scan.get("scan_results", {}).get("confirmation_bias_indicators", 0) +
                scan.get("scan_results", {}).get("availability_bias_indicators", 0) +
                scan.get("scan_results", {}).get("anchoring_bias_indicators", 0)
                for scan in recent_scans
            )

            return {
                "total_bias_scans": len(recent_scans),
                "total_bias_indicators": total_bias_indicators,
                "bias_rate": (total_bias_indicators / len(recent_scans)) if recent_scans else 0,
                "bias_trend": "improving" if total_bias_indicators < 5 else "needs_attention"
            }

        except Exception:
            return {"status": "bias_analysis_error"}

    def _analyze_dilemma_resolution(self) -> Dict[str, Any]:
        """Analyze ethical dilemma resolution patterns"""
        try:
            if not self.ethical_dilemmas:
                return {"status": "no_dilemmas"}

            recent_dilemmas = self.ethical_dilemmas[-20:]

            resolution_types = {}
            for dilemma in recent_dilemmas:
                resolution = dilemma.get("resolution", {}).get("resolution", "unknown")
                resolution_types[resolution] = resolution_types.get(resolution, 0) + 1

            return {
                "total_dilemmas": len(recent_dilemmas),
                "resolution_breakdown": resolution_types,
                "most_common_resolution": max(resolution_types.items(), key=lambda x: x[1])[0] if resolution_types else "unknown",
                "average_resolution_time": sum(d.get("resolution", {}).get("time_taken", 0) for d in recent_dilemmas) / len(recent_dilemmas)
            }

        except Exception:
            return {"status": "dilemma_analysis_error"}

    def _generate_ethical_recommendations(self) -> List[str]:
        """Generate ethical recommendations"""
        try:
            recommendations = []

            # Based on compliance score
            if self.ethical_compliance_score < 70:
                recommendations.append("Strengthen ethical decision-making processes")
                recommendations.append("Increase ethical training and awareness")

            # Based on bias detection
            if self.bias_detection_results:
                recent_bias = self.bias_detection_results[-1]
                total_bias = sum(recent_bias.get("scan_results", {}).values()) - recent_bias.get("scan_results", {}).get("scanned_decisions", 0)
                if total_bias > 2:
                    recommendations.append("Implement additional bias detection and mitigation strategies")

            # Based on principle compliance
            principle_compliance = self.value_alignment_metrics.get("principle_compliance", {})
            if principle_compliance:
                weakest_principle = min(principle_compliance.items(), key=lambda x: x[1])
                if weakest_principle[1] < 60:
                    recommendations.append(f"Strengthen compliance with {weakest_principle[0]} principle")

            if not recommendations:
                recommendations.append("Continue current ethical practices")
                recommendations.append("Regular ethical self-assessment is recommended")

            return recommendations

        except Exception:
            return ["Conduct comprehensive ethical review"]

    def shutdown(self):
        """Graceful shutdown with ethical data preservation"""
        print("⚖️  ETHICAL FRAMEWORK SHUTTING DOWN...")
        print("💾 Saving ethical data...")

        try:
            # Save ethical data
            ethical_data = {
                "decision_history": self.decision_history[-100:],  # Save last 100 decisions
                "ethical_dilemmas": self.ethical_dilemmas[-50:],  # Save last 50 dilemmas
                "value_alignment_metrics": self.value_alignment_metrics,
                "bias_detection_results": self.bias_detection_results[-20:],  # Save last 20 bias scans
                "transparency_log": self.transparency_log[-100:],  # Save last 100 log entries
                "ethical_compliance_score": self.ethical_compliance_score,
                "saved_at": datetime.now().isoformat()
            }

            with open("ethical_framework_data.json", 'w') as f:
                json.dump(ethical_data, f, indent=2)

            print("✅ Ethical data saved")

        except Exception as e:
            print(f"⚠️  Ethical data save error: {e}")

        self.monitoring_active = False
        print("✅ Ethical framework shutdown complete")

# Global ethical framework instance
ethical_framework = None

def initialize_ethical_framework():
    """Initialize the Ethical Framework"""
    global ethical_framework
    if ethical_framework is None:
        ethical_framework = EthicalFramework()
    return ethical_framework

def evaluate_decision(decision_context):
    """Evaluate ethics of a decision"""
    if ethical_framework:
        return ethical_framework.evaluate_decision_ethics(decision_context)
    else:
        return {"decision": "requires_review", "reasoning": "Ethical framework not initialized"}

def get_ethical_status():
    """Get ethical framework status"""
    if ethical_framework:
        return ethical_framework.get_ethical_status()
    else:
        return {"status": "ethical_framework_not_initialized"}

def get_ethical_report():
    """Generate comprehensive ethical report"""
    if ethical_framework:
        return ethical_framework.get_ethical_report()
    else:
        return {"status": "ethical_framework_not_initialized"}

def resolve_dilemma(dilemma_context):
    """Resolve an ethical dilemma"""
    if ethical_framework:
        return ethical_framework.resolve_ethical_dilemma(dilemma_context)
    else:
        return {"resolution": "requires_human_intervention", "reasoning": "Ethical framework not initialized"}

# Auto-initialize when imported
if __name__ == "__main__":
    print("⚖️  ETHICAL FRAMEWORK")
    print("=" * 25)
    ethics = initialize_ethical_framework()

    # Demonstration loop
    try:
        while True:
            status = ethics.get_ethical_status()
            print(f"\n⚖️  ETHICAL STATUS: Compliance={status['ethical_compliance_score']:.1f}%, Decisions={status['recent_decisions_count']}")

            # Evaluate a sample decision
            sample_decision = {
                "description": "Deploy new feature that improves user experience but requires additional data collection",
                "stakeholders": ["users", "privacy_officer", "development_team"],
                "potential_benefits": ["better_user_experience", "increased_engagement"],
                "potential_risks": ["privacy_concerns", "data_security_risks"]
            }

            result = ethics.evaluate_decision_ethics(sample_decision)
            print(f"🤝 Decision Evaluation: {result['decision']} ({result['confidence']}% confidence)")

            # Generate ethical report periodically
            if random.random() < 0.2:  # 20% chance each cycle
                report = ethics.get_ethical_report()
                if 'decision_analysis' in report:
                    analysis = report['decision_analysis']
                    if analysis.get('approval_rate') is not None:
                        print(f"📋 Ethical Report: {analysis['approval_rate']:.1f}% approval rate")

            time.sleep(15)

    except KeyboardInterrupt:
        print("\n🛑 Shutting down ethical framework...")
        ethics.shutdown()
