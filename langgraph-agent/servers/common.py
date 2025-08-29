"""COMMON MCP Server - 🏠 In-house abilities for customer support workflow.
Handles internal logic that doesn't require external systems.
"""

from typing import Dict, Any
import logging
from datetime import datetime, timedelta
import re
from enum import Enum
from pydantic import BaseModel
from typing import List, Optional

class ResolutionStatus(str, Enum):
    PENDING = "pending"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

class SLACompliance(BaseModel):
    met: bool
    response_time_minutes: float
    target_time_minutes: float

class NextAction(BaseModel):
    action: str
    priority: str
    due_date: str

class CustomerSupportPayload(BaseModel):
    case_id: str
    customer_id: str
    resolution_status: ResolutionStatus
    response_text: str
    escalation_required: bool
    sla_compliance: SLACompliance
    next_actions: List[NextAction]

logger = logging.getLogger(__name__)


class CommonServerAbilities:
    """COMMON MCP server abilities for customer support workflow."""
    
    def get_abilities(self) -> List[str]:
        """Return list of available internal abilities"""
        return [
            "accept_payload",
            "validate_input", 
            "normalize_fields",
            "parse_request_text",
            "add_flags_calculations",
            "response_generation",
            "output_payload",
            "check_required_fields",
            "check_permissions",
            "extract_entities",
            "enrich_records",
            "escalation_decision",
            "solution_evaluation",
            "update_payload"
        ]
    
    def accept_payload(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Accept and log the incoming payload."""
        logger.info("        📥 Accepting customer support payload")
        
        return {
            'payload_accepted': True,
            'payload_timestamp': datetime.now().isoformat(),
            'payload_size': len(str(state))
        }
    
    def validate_input(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Validate required fields in the input."""
        logger.info("        🔍 Validating input fields")
        
        required_fields = ['customer', 'query', 'ticket_id']
        validation_results = {}
        
        for field in required_fields:
            validation_results[f'{field}_valid'] = field in state and state[field] is not None
        
        all_valid = all(validation_results.values())
        
        return {
            'input_validation': validation_results,
            'validation_passed': all_valid,
            'validation_timestamp': datetime.now().isoformat()
        }
    
    def normalize_fields(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize and clean data fields."""
        logger.info("        🧹 Normalizing data fields")
        
        normalized = {}
        
        # Normalize customer name
        if 'customer' in state and 'name' in state['customer']:
            normalized['customer_name_normalized'] = state['customer']['name'].strip().title()
        
        # Normalize query text
        if 'query' in state:
            normalized['query_normalized'] = re.sub(r'\s+', ' ', state['query'].strip())
            normalized['query_length'] = len(normalized['query_normalized'])
        
        # Normalize ticket ID
        if 'ticket_id' in state:
            normalized['ticket_id_normalized'] = str(state['ticket_id']).upper().strip()
        
        return {
            'normalization': normalized,
            'normalization_timestamp': datetime.now().isoformat()
        }
    
    def categorize_request(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Categorize the support request based on query content."""
        logger.info("        📂 Categorizing support request")
        
        query = state.get('query_normalized', state.get('query', '')).lower()
        
        # Simple categorization logic
        if any(word in query for word in ['password', 'login', 'access', 'account']):
            category = 'account_access'
        elif any(word in query for word in ['billing', 'payment', 'invoice', 'charge']):
            category = 'billing'
        elif any(word in query for word in ['bug', 'error', 'broken', 'not working']):
            category = 'technical_issue'
        elif any(word in query for word in ['feature', 'request', 'enhancement']):
            category = 'feature_request'
        else:
            category = 'general_inquiry'
        
        return {
            'request_category': category,
            'category_confidence': 0.8,
            'categorization_timestamp': datetime.now().isoformat()
        }
    
    def calculate_sla_risk(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate SLA risk based on priority and timing."""
        logger.info("        ⏰ Calculating SLA risk")
        
        priority = state.get('priority', 'medium').lower()
        category = state.get('request_category', 'general_inquiry')
        
        # SLA targets (in hours)
        sla_targets = {
            'high': 4,
            'medium': 24,
            'low': 72
        }
        
        target_hours = sla_targets.get(priority, 24)
        current_time = datetime.now()
        
        # Calculate risk score (0-1, where 1 is highest risk)
        if category == 'billing':
            risk_multiplier = 1.2
        elif category == 'technical_issue':
            risk_multiplier = 1.1
        else:
            risk_multiplier = 1.0
        
        base_risk = 0.3 if priority == 'high' else 0.1
        sla_risk_score = min(base_risk * risk_multiplier, 1.0)
        
        return {
            'sla_target_hours': target_hours,
            'sla_risk_score': sla_risk_score,
            'sla_deadline': (current_time + timedelta(hours=target_hours)).isoformat(),
            'sla_calculation_timestamp': current_time.isoformat()
        }
    
    def assess_priority(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Assess and potentially adjust request priority."""
        logger.info("        🎯 Assessing request priority")
        
        original_priority = state.get('priority', 'medium')
        category = state.get('request_category', 'general_inquiry')
        customer_tier = state.get('customer', {}).get('tier', 'standard')
        
        # Priority adjustment logic
        priority_score = 0.5  # Base score
        
        if customer_tier == 'premium':
            priority_score += 0.2
        elif customer_tier == 'enterprise':
            priority_score += 0.3
        
        if category in ['billing', 'account_access']:
            priority_score += 0.2
        elif category == 'technical_issue':
            priority_score += 0.1
        
        # Determine final priority
        if priority_score >= 0.8:
            final_priority = 'high'
        elif priority_score >= 0.4:
            final_priority = 'medium'
        else:
            final_priority = 'low'
        
        return {
            'original_priority': original_priority,
            'final_priority': final_priority,
            'priority_score': priority_score,
            'priority_adjusted': final_priority != original_priority,
            'priority_assessment_timestamp': datetime.now().isoformat()
        }
    
    def draft_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Draft an initial response based on the analysis."""
        logger.info("        ✍️  Drafting response")
        
        customer_name = state.get('customer_name_normalized', 'Valued Customer')
        category = state.get('request_category', 'general_inquiry')
        
        # Template responses based on category
        templates = {
            'account_access': f"Dear {customer_name}, I understand you're experiencing issues with account access. Let me help you resolve this quickly.",
            'billing': f"Dear {customer_name}, Thank you for contacting us about your billing inquiry. I'll review your account and provide clarification.",
            'technical_issue': f"Dear {customer_name}, I see you're experiencing a technical issue. Let me investigate this for you right away.",
            'feature_request': f"Dear {customer_name}, Thank you for your feature suggestion. I'll make sure this reaches our product team.",
            'general_inquiry': f"Dear {customer_name}, Thank you for reaching out. I'm here to help with your inquiry."
        }
        
        draft_response = templates.get(category, templates['general_inquiry'])
        
        return {
            'draft_response': draft_response,
            'response_template': category,
            'response_length': len(draft_response),
            'draft_timestamp': datetime.now().isoformat()
        }

    def execute_ability(self, ability_name, data):
        """Execute a specific ability by name"""
        if hasattr(self, ability_name):
            method = getattr(self, ability_name)
            return method(data)
        else:
            raise AttributeError(f"Unknown ability: {ability_name}")

    # Missing abilities implementation
    def check_required_fields(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Check if all required fields are present and valid."""
        logger.info("        ✅ Checking required fields")
        
        required_fields = {
            'customer_id': str,
            'request': dict,
            'contact_info': dict
        }
        
        missing_fields = []
        invalid_types = []
        
        for field, expected_type in required_fields.items():
            if field not in state:
                missing_fields.append(field)
            elif not isinstance(state[field], expected_type):
                invalid_types.append(field)
        
        return {
            'required_fields_check': {
                'missing_fields': missing_fields,
                'invalid_types': invalid_types,
                'all_required_present': len(missing_fields) == 0 and len(invalid_types) == 0
            },
            'check_timestamp': datetime.now().isoformat()
        }
    
    def sanitize_data(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize input data to prevent security issues."""
        logger.info("        🧼 Sanitizing input data")
        
        sanitized_data = {}
        
        # Sanitize customer ID
        if 'customer_id' in state:
            sanitized_data['customer_id'] = re.sub(r'[^a-zA-Z0-9-_]', '', str(state['customer_id']))
        
        # Sanitize request description
        if 'request' in state and 'description' in state['request']:
            description = state['request']['description']
            # Remove potential script tags and normalize whitespace
            sanitized_description = re.sub(r'<script[^>]*>.*?</script>', '', description, flags=re.IGNORECASE)
            sanitized_description = re.sub(r'\s+', ' ', sanitized_description).strip()
            sanitized_data['sanitized_description'] = sanitized_description
        
        # Sanitize email
        if 'contact_info' in state and 'email' in state['contact_info']:
            email = state['contact_info']['email']
            # Basic email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            sanitized_data['email_valid'] = bool(re.match(email_pattern, email))
        
        return {
            'sanitized_data': sanitized_data,
            'sanitization_timestamp': datetime.now().isoformat()
        }
    
    def authenticate_customer(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Authenticate customer identity."""
        logger.info("        🔐 Authenticating customer")
        
        customer_id = state.get('customer_id')
        contact_info = state.get('contact_info', {})
        
        # Simulate authentication logic
        auth_factors = []
        
        if customer_id:
            auth_factors.append('customer_id_provided')
        
        if contact_info.get('email'):
            auth_factors.append('email_verified')
        
        if contact_info.get('phone'):
            auth_factors.append('phone_verified')
        
        # Determine authentication level
        if len(auth_factors) >= 2:
            auth_level = 'high'
        elif len(auth_factors) == 1:
            auth_level = 'medium'
        else:
            auth_level = 'low'
        
        return {
            'authentication': {
                'auth_level': auth_level,
                'auth_factors': auth_factors,
                'authenticated': len(auth_factors) > 0
            },
            'auth_timestamp': datetime.now().isoformat()
        }
    
    def check_permissions(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Check customer permissions and access levels."""
        logger.info("        🔑 Checking permissions")
        
        customer_context = state.get('customer_context', {})
        account_type = customer_context.get('account_type', 'standard')
        subscription_tier = customer_context.get('subscription_tier', 'basic')
        
        permissions = {
            'can_access_support': True,
            'can_escalate': account_type in ['enterprise', 'premium'],
            'priority_support': subscription_tier in ['premium', 'enterprise'],
            'api_access': account_type == 'enterprise',
            'billing_access': True
        }
        
        return {
            'permissions': permissions,
            'account_type': account_type,
            'subscription_tier': subscription_tier,
            'permissions_timestamp': datetime.now().isoformat()
        }
    
    def verify_account_status(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Verify customer account status."""
        logger.info("        ✔️ Verifying account status")
        
        customer_context = state.get('customer_context', {})
        contract_details = customer_context.get('contract_details', {})
        
        # Simulate account status check
        account_status = {
            'active': True,
            'in_good_standing': True,
            'contract_valid': bool(contract_details.get('contract_id')),
            'sla_active': contract_details.get('support_level') == '24x7_premium',
            'payment_current': True
        }
        
        overall_status = 'active' if all(account_status.values()) else 'restricted'
        
        return {
            'account_status': account_status,
            'overall_status': overall_status,
            'status_timestamp': datetime.now().isoformat()
        }
    
    def classify_intent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Classify customer intent from the request."""
        logger.info("        🎯 Classifying customer intent")
        
        request = state.get('request', {})
        description = request.get('description', '').lower()
        subject = request.get('subject', '').lower()
        
        text_to_analyze = f"{subject} {description}"
        
        # Intent classification logic
        intent_keywords = {
            'get_help': ['help', 'support', 'assistance', 'problem', 'issue'],
            'report_bug': ['bug', 'error', 'broken', 'not working', 'failure'],
            'request_feature': ['feature', 'enhancement', 'improvement', 'add'],
            'billing_inquiry': ['billing', 'payment', 'invoice', 'charge', 'refund'],
            'account_access': ['login', 'password', 'access', 'locked', 'reset'],
            'cancel_service': ['cancel', 'terminate', 'stop', 'end service'],
            'upgrade_service': ['upgrade', 'premium', 'enterprise', 'more features']
        }
        
        intent_scores = {}
        for intent, keywords in intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_to_analyze)
            if score > 0:
                intent_scores[intent] = score / len(keywords)
        
        primary_intent = max(intent_scores.items(), key=lambda x: x[1])[0] if intent_scores else 'general_inquiry'
        confidence = intent_scores.get(primary_intent, 0.1)
        
        return {
            'intent_classification': {
                'primary_intent': primary_intent,
                'confidence': confidence,
                'all_intents': intent_scores
            },
            'classification_timestamp': datetime.now().isoformat()
        }
    
    def determine_category(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Determine support category based on intent and content."""
        logger.info("        📋 Determining support category")
        
        intent_data = state.get('intent_classification', {})
        primary_intent = intent_data.get('primary_intent', 'general_inquiry')
        
        # Map intents to categories
        intent_to_category = {
            'get_help': 'technical_support',
            'report_bug': 'technical_support',
            'request_feature': 'product_feedback',
            'billing_inquiry': 'billing_support',
            'account_access': 'account_support',
            'cancel_service': 'account_management',
            'upgrade_service': 'sales_support',
            'general_inquiry': 'general_support'
        }
        
        category = intent_to_category.get(primary_intent, 'general_support')
        
        # Determine routing priority
        priority_categories = ['technical_support', 'billing_support', 'account_support']
        routing_priority = 'high' if category in priority_categories else 'normal'
        
        return {
            'support_category': {
                'category': category,
                'routing_priority': routing_priority,
                'based_on_intent': primary_intent
            },
            'category_timestamp': datetime.now().isoformat()
        }
    
    def personalize_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Personalize response based on customer profile."""
        logger.info("        👤 Personalizing response")
        
        customer_context = state.get('customer_context', {})
        contact_info = state.get('contact_info', {})
        
        # Extract personalization data
        customer_name = contact_info.get('preferred_name', 'Valued Customer')
        account_type = customer_context.get('account_type', 'standard')
        previous_interactions = customer_context.get('previous_interactions', [])
        
        # Personalization elements
        personalization = {
            'greeting': f"Hello {customer_name}",
            'account_acknowledgment': f"As a {account_type} customer" if account_type != 'standard' else '',
            'history_reference': len(previous_interactions) > 0,
            'tone': 'formal' if account_type == 'enterprise' else 'friendly'
        }
        
        # Generate personalized opening
        if previous_interactions:
            last_interaction = previous_interactions[-1]
            if last_interaction.get('satisfaction_score', 0) >= 4.0:
                personalization['reference_note'] = "Thank you for your continued trust in our service."
        
        return {
            'personalization': personalization,
            'personalization_timestamp': datetime.now().isoformat()
        }
    
    def check_compliance(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Check compliance requirements for the request."""
        logger.info("        📜 Checking compliance requirements")
        
        business_impact = state.get('business_impact', {})
        customer_context = state.get('customer_context', {})
        
        compliance_checks = {
            'data_privacy': True,  # Always ensure data privacy
            'gdpr_applicable': customer_context.get('region') in ['EU', 'Europe'],
            'security_review_needed': business_impact.get('compliance_risk') == 'high',
            'audit_trail_required': business_impact.get('severity') == 'high',
            'escalation_documented': True
        }
        
        compliance_score = sum(compliance_checks.values()) / len(compliance_checks)
        
        return {
            'compliance_check': {
                'checks': compliance_checks,
                'compliance_score': compliance_score,
                'compliant': compliance_score >= 0.8
            },
            'compliance_timestamp': datetime.now().isoformat()
        }
    
    def validate_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the generated response for quality and accuracy."""
        logger.info("        ✅ Validating response quality")
        
        draft_response = state.get('draft_response', '')
        personalization = state.get('personalization', {})
        
        validation_results = {
            'has_greeting': personalization.get('greeting', '') in draft_response,
            'appropriate_length': 50 <= len(draft_response) <= 500,
            'professional_tone': not any(word in draft_response.lower() for word in ['sorry', 'unfortunately', 'can\'t']),
            'includes_next_steps': any(phrase in draft_response.lower() for phrase in ['will', 'next', 'follow up']),
            'personalized': bool(personalization.get('greeting'))
        }
        
        validation_score = sum(validation_results.values()) / len(validation_results)
        
        return {
            'response_validation': {
                'validation_results': validation_results,
                'validation_score': validation_score,
                'response_approved': validation_score >= 0.6
            },
            'validation_timestamp': datetime.now().isoformat()
        }
    
    def verify_accuracy(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Verify accuracy of information and recommendations."""
        logger.info("        🔍 Verifying information accuracy")
        
        support_category = state.get('support_category', {})
        suggested_actions = state.get('suggested_actions', [])
        
        accuracy_checks = {
            'category_matches_intent': True,  # Assume correct for demo
            'actions_relevant': len(suggested_actions) > 0,
            'information_current': True,
            'no_contradictions': True,
            'sources_verified': True
        }
        
        accuracy_score = sum(accuracy_checks.values()) / len(accuracy_checks)
        
        return {
            'accuracy_verification': {
                'checks': accuracy_checks,
                'accuracy_score': accuracy_score,
                'verified': accuracy_score >= 0.8
            },
            'verification_timestamp': datetime.now().isoformat()
        }
    
    def assess_escalation_need(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Assess if the request needs escalation."""
        logger.info("        🔺 Assessing escalation need")
        
        business_impact = state.get('business_impact', {})
        customer_context = state.get('customer_context', {})
        support_category = state.get('support_category', {})
        
        escalation_factors = {
            'high_severity': business_impact.get('severity') == 'high',
            'premium_customer': customer_context.get('subscription_tier') == 'premium',
            'technical_complexity': support_category.get('category') == 'technical_support',
            'revenue_impact': business_impact.get('revenue_impact', '').startswith('$'),
            'sla_risk': state.get('sla_risk_score', 0) > 0.7
        }
        
        escalation_score = sum(escalation_factors.values()) / len(escalation_factors)
        needs_escalation = escalation_score >= 0.4
        
        escalation_level = 'immediate' if escalation_score >= 0.8 else 'standard' if needs_escalation else 'none'
        
        return {
            'escalation_assessment': {
                'factors': escalation_factors,
                'escalation_score': escalation_score,
                'needs_escalation': needs_escalation,
                'escalation_level': escalation_level
            },
            'assessment_timestamp': datetime.now().isoformat()
        }
    
    def determine_priority(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Determine final priority based on all factors."""
        logger.info("        🎯 Determining final priority")
        
        escalation_assessment = state.get('escalation_assessment', {})
        business_impact = state.get('business_impact', {})
        customer_context = state.get('customer_context', {})
        
        priority_factors = {
            'business_impact': business_impact.get('severity', 'medium'),
            'customer_tier': customer_context.get('subscription_tier', 'standard'),
            'escalation_level': escalation_assessment.get('escalation_level', 'none'),
            'affected_users': business_impact.get('affected_users', 0)
        }
        
        # Calculate priority score
        priority_score = 0
        
        if priority_factors['business_impact'] == 'high':
            priority_score += 3
        elif priority_factors['business_impact'] == 'medium':
            priority_score += 2
        else:
            priority_score += 1
        
        if priority_factors['customer_tier'] in ['premium', 'enterprise']:
            priority_score += 2
        
        if priority_factors['escalation_level'] == 'immediate':
            priority_score += 3
        elif priority_factors['escalation_level'] == 'standard':
            priority_score += 1
        
        if priority_factors['affected_users'] > 1000:
            priority_score += 2
        
        # Determine final priority
        if priority_score >= 7:
            final_priority = 'critical'
        elif priority_score >= 5:
            final_priority = 'high'
        elif priority_score >= 3:
            final_priority = 'medium'
        else:
            final_priority = 'low'
        
        return {
            'priority_determination': {
                'factors': priority_factors,
                'priority_score': priority_score,
                'final_priority': final_priority
            },
            'priority_timestamp': datetime.now().isoformat()
        }
    
    def route_to_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Route request to appropriate human agent."""
        logger.info("        🎯 Routing to agent")
        
        escalation_need = state.get('escalation_need', {})
        priority_level = state.get('priority_level', {})
        support_category = state.get('support_category', {})
        
        # Determine agent type based on category and complexity
        category = support_category.get('category', 'general')
        priority = priority_level.get('priority', 'medium')
        
        agent_routing = {
            'technical_support': 'technical_specialist',
            'billing_support': 'billing_specialist', 
            'account_support': 'account_manager',
            'general': 'general_support'
        }
        
        assigned_agent_type = agent_routing.get(category, 'general_support')
        
        # Priority-based queue assignment
        queue_priority = {
            'critical': 1,
            'high': 2, 
            'medium': 3,
            'low': 4
        }.get(priority, 3)
        
        return {
            'agent_routing': {
                'agent_type': assigned_agent_type,
                'queue_priority': queue_priority,
                'estimated_wait_time': f"{queue_priority * 5}-{queue_priority * 10} minutes",
                'routing_reason': escalation_need.get('reason', 'standard_routing')
            },
            'routing_timestamp': datetime.now().isoformat()
        }

    def assess_complexity(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the complexity of the customer request."""
        logger.info("        🧠 Assessing request complexity")
        
        request = state.get('request', {})
        customer_context = state.get('customer_context', {})
        business_impact = state.get('business_impact', {})
        
        # Complexity factors
        complexity_factors = {
            'technical_depth': len(request.get('description', '').split()) > 100,
            'multiple_systems': 'integration' in request.get('description', '').lower(),
            'high_business_impact': business_impact.get('severity') == 'high',
            'enterprise_customer': customer_context.get('account_type') == 'enterprise',
            'has_attachments': len(request.get('attachments', [])) > 0,
            'urgent_timeline': request.get('urgency') == 'critical'
        }
        
        complexity_score = sum(complexity_factors.values()) / len(complexity_factors)
        
        # Determine complexity level
        if complexity_score >= 0.7:
            complexity_level = 'high'
        elif complexity_score >= 0.4:
            complexity_level = 'medium'
        else:
            complexity_level = 'low'
        
        return {
            'complexity_assessment': {
                'factors': complexity_factors,
                'complexity_score': complexity_score,
                'complexity_level': complexity_level,
                'requires_specialist': complexity_level == 'high'
            },
            'complexity_timestamp': datetime.now().isoformat()
        }

    def rank_recommendations(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Rank solution recommendations by relevance and effectiveness."""
        logger.info("        📊 Ranking solution recommendations")
        
        solutions = state.get('generated_solutions', [])
        customer_context = state.get('customer_context', {})
        complexity_assessment = state.get('complexity_assessment', {})
        
        # Ranking criteria weights
        ranking_weights = {
            'relevance': 0.3,
            'implementation_ease': 0.2,
            'customer_preference': 0.2,
            'success_rate': 0.2,
            'time_to_resolution': 0.1
        }
        
        ranked_solutions = []
        for i, solution in enumerate(solutions):
            # Mock scoring based on solution characteristics
            scores = {
                'relevance': 0.9 - (i * 0.1),  # First solutions more relevant
                'implementation_ease': 0.8 if 'simple' in str(solution).lower() else 0.6,
                'customer_preference': 0.9 if customer_context.get('account_type') == 'premium' else 0.7,
                'success_rate': 0.85,  # Historical success rate
                'time_to_resolution': 0.7 if complexity_assessment.get('complexity_level') == 'low' else 0.5
            }
            
            # Calculate weighted score
            weighted_score = sum(scores[criterion] * ranking_weights[criterion] 
                               for criterion in ranking_weights)
            
            ranked_solutions.append({
                'solution': solution,
                'rank': i + 1,
                'weighted_score': weighted_score,
                'individual_scores': scores
            })
        
        # Sort by weighted score (descending)
        ranked_solutions.sort(key=lambda x: x['weighted_score'], reverse=True)
        
        # Update ranks after sorting
        for i, solution in enumerate(ranked_solutions):
            solution['rank'] = i + 1
        
        return {
            'ranked_recommendations': {
                'solutions': ranked_solutions,
                'ranking_criteria': ranking_weights,
                'total_solutions': len(ranked_solutions)
            },
            'ranking_timestamp': datetime.now().isoformat()
        }

    def generate_solution(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate tailored solutions based on customer request and context."""
        logger.info("        💡 Generating tailored solutions")
        
        request = state.get('request', {})
        customer_context = state.get('customer_context', {})
        support_category = state.get('support_category', {})
        complexity_assessment = state.get('complexity_assessment', {})
        
        category = support_category.get('category', 'general')
        complexity = complexity_assessment.get('complexity_level', 'medium')
        
        # Solution templates based on category
        solution_templates = {
            'technical_support': [
                "Check system configuration and restart services",
                "Update to latest version and clear cache", 
                "Review API documentation and verify endpoints",
                "Contact technical team for advanced troubleshooting"
            ],
            'billing_support': [
                "Review account billing history and charges",
                "Process refund or credit adjustment",
                "Update payment method and retry transaction",
                "Escalate to billing specialist for complex issues"
            ],
            'account_support': [
                "Verify account credentials and reset if needed",
                "Update account information and preferences",
                "Review account permissions and access levels",
                "Coordinate with account manager for enterprise needs"
            ],
            'general': [
                "Provide step-by-step guidance",
                "Share relevant documentation links",
                "Schedule follow-up consultation",
                "Escalate to appropriate specialist"
            ]
        }
        
        base_solutions = solution_templates.get(category, solution_templates['general'])
        
        # Customize solutions based on complexity and customer type
        generated_solutions = []
        for solution in base_solutions:
            customized_solution = {
                'description': solution,
                'complexity_match': complexity,
                'estimated_time': self._estimate_solution_time(solution, complexity),
                'requires_escalation': complexity == 'high' and 'escalate' not in solution.lower(),
                'customer_type_optimized': customer_context.get('account_type', 'standard')
            }
            generated_solutions.append(customized_solution)
        
        return {
            'generated_solutions': generated_solutions,
            'solution_metadata': {
                'category': category,
                'complexity_level': complexity,
                'total_solutions': len(generated_solutions),
                'customization_applied': True
            },
            'generation_timestamp': datetime.now().isoformat()
        }
    
    def _estimate_solution_time(self, solution: str, complexity: str) -> str:
        """Estimate time required to implement solution."""
        base_times = {
            'low': 15,
            'medium': 45, 
            'high': 120
        }
        
        base_time = base_times.get(complexity, 45)
        
        # Adjust based on solution length
        if len(solution) > 200:
            base_time *= 1.5
        elif len(solution) < 50:
            base_time *= 0.7
        
        return f"{base_time} minutes"
    
    def parse_request_text(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and extract key information from request text."""
        logger.info("        📝 Parsing request text")
        
        query = state.get('query', '')
        request_text = state.get('request', {}).get('text', query)
        
        # Extract key phrases and entities
        keywords = []
        urgency_indicators = ['urgent', 'asap', 'immediately', 'critical', 'emergency']
        
        text_lower = request_text.lower()
        for indicator in urgency_indicators:
            if indicator in text_lower:
                keywords.append(indicator)
        
        # Extract potential product/service mentions
        products = ['account', 'billing', 'payment', 'login', 'password', 'feature']
        mentioned_products = [prod for prod in products if prod in text_lower]
        
        return {
            'parsed_request': {
                'original_text': request_text,
                'keywords': keywords,
                'mentioned_products': mentioned_products,
                'text_length': len(request_text),
                'urgency_detected': len(keywords) > 0
            },
            'parsing_timestamp': datetime.now().isoformat()
        }
    
    def add_flags_calculations(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Add flags and calculations based on request analysis."""
        logger.info("        🚩 Adding flags and calculations")
        
        flags = {
            'high_priority': False,
            'requires_escalation': False,
            'potential_churn_risk': False,
            'technical_issue': False,
            'billing_related': False
        }
        
        # Analyze request content for flags
        query = state.get('query', '').lower()
        parsed_request = state.get('parsed_request', {})
        
        # High priority flag
        if parsed_request.get('urgency_detected') or 'high' in state.get('priority', '').lower():
            flags['high_priority'] = True
        
        # Technical issue flag
        tech_keywords = ['error', 'bug', 'broken', 'not working', 'crash', 'issue']
        if any(keyword in query for keyword in tech_keywords):
            flags['technical_issue'] = True
        
        # Billing related flag
        billing_keywords = ['billing', 'payment', 'charge', 'invoice', 'refund']
        if any(keyword in query for keyword in billing_keywords):
            flags['billing_related'] = True
        
        # Escalation flag
        escalation_keywords = ['manager', 'supervisor', 'complaint', 'unsatisfied']
        if any(keyword in query for keyword in escalation_keywords):
            flags['requires_escalation'] = True
        
        # Calculate risk score
        risk_score = 0
        if flags['high_priority']: risk_score += 30
        if flags['requires_escalation']: risk_score += 40
        if flags['technical_issue']: risk_score += 20
        if flags['billing_related']: risk_score += 15
        
        return {
            'flags': flags,
            'calculations': {
                'risk_score': min(risk_score, 100),
                'complexity_estimate': 'high' if risk_score > 60 else 'medium' if risk_score > 30 else 'low'
            },
            'flags_timestamp': datetime.now().isoformat()
        }
    
    def response_generation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate appropriate response based on request analysis."""
        logger.info("        💬 Generating response")
        
        # Get context from state
        customer_name = state.get('customer', {}).get('name', 'Valued Customer')
        request_category = state.get('request_category', 'general_inquiry')
        flags = state.get('flags', {})
        solution = state.get('solution', {})
        
        # Generate personalized response
        greeting = f"Dear {customer_name},"
        
        # Category-specific responses
        if request_category == 'account_access':
            response_body = "Thank you for contacting us regarding your account access. We understand how important it is to have seamless access to your account."
        elif request_category == 'billing':
            response_body = "Thank you for reaching out about your billing inquiry. We're here to help resolve any billing-related concerns you may have."
        elif request_category == 'technical_issue':
            response_body = "Thank you for reporting this technical issue. We take all technical concerns seriously and will work to resolve this promptly."
        elif request_category == 'feature_request':
            response_body = "Thank you for your feature suggestion. We value customer feedback and will consider your request for future improvements."
        else:
            response_body = "Thank you for contacting us. We have received your inquiry and will provide you with the assistance you need."
        
        # Add solution if available
        if solution.get('description'):
            response_body += f" Based on your request, {solution['description']}"
        
        # Add escalation notice if needed
        if flags.get('requires_escalation'):
            response_body += " Your case has been escalated to our specialized team for further assistance."
        
        # Closing
        closing = "If you have any additional questions, please don't hesitate to reach out. We're here to help!\n\nBest regards,\nCustomer Support Team"
        
        full_response = f"{greeting}\n\n{response_body}\n\n{closing}"
        
        return {
            'response_text': full_response,
            'response_metadata': {
                'category': request_category,
                'personalized': True,
                'escalated': flags.get('requires_escalation', False),
                'solution_included': bool(solution.get('description'))
            },
            'generation_timestamp': datetime.now().isoformat()
        }
    
    def output_payload(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured JSON output payload according to LangGraph specification."""
        logger.info("        📤 Generating structured output payload")
        
        # Extract or generate required fields from state
        case_id = state.get('case_id', f"case_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        customer_id = state.get('customer', {}).get('id', state.get('customer_id', 'unknown'))
        
        # Determine resolution status based on workflow state
        escalation_required = state.get('escalation_required', False)
        if escalation_required:
            resolution_status = ResolutionStatus.ESCALATED
        elif state.get('workflow_status') == 'completed':
            resolution_status = ResolutionStatus.RESOLVED
        elif state.get('workflow_status') == 'failed':
            resolution_status = ResolutionStatus.PENDING
        else:
            resolution_status = ResolutionStatus.PENDING
        
        # Generate response text
        response_text = state.get('final_response', state.get('response_text', 
            "Thank you for contacting us. We have processed your request and will follow up as needed."))
        
        # Calculate SLA compliance
        start_time_str = state.get('start_time')
        current_time = datetime.now()
        
        if start_time_str:
            try:
                start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
                response_time_minutes = (current_time - start_time).total_seconds() / 60
            except:
                response_time_minutes = 0.0
        else:
            response_time_minutes = 0.0
        
        # Determine target time based on priority
        priority = state.get('priority', 'medium')
        target_times = {'high': 60, 'medium': 240, 'low': 480}  # minutes
        target_time_minutes = target_times.get(priority, 240)
        
        sla_compliance = SLACompliance(
            met=response_time_minutes <= target_time_minutes,
            response_time_minutes=response_time_minutes,
            target_time_minutes=target_time_minutes
        )
        
        # Generate next actions
        next_actions = []
        
        if escalation_required:
            next_actions.append(NextAction(
                action="escalate_to_specialist",
                priority="high",
                due_date=(current_time + timedelta(hours=2)).isoformat()
            ))
        
        if state.get('follow_up_required', True):
            next_actions.append(NextAction(
                action="follow_up_with_customer",
                priority="medium",
                due_date=(current_time + timedelta(days=1)).isoformat()
            ))
        
        # Create the structured payload
        try:
            payload = CustomerSupportPayload(
                case_id=case_id,
                customer_id=customer_id,
                resolution_status=resolution_status,
                response_text=response_text,
                escalation_required=escalation_required,
                sla_compliance=sla_compliance,
                next_actions=next_actions
            )
            
            return {
                'structured_payload': payload.dict(),
                'payload_generated': True,
                'generation_timestamp': current_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error creating structured payload: {e}")
            # Fallback to basic structure
            return {
                'structured_payload': {
                    'case_id': case_id,
                    'customer_id': customer_id,
                    'resolution_status': 'pending',
                    'response_text': response_text,
                    'escalation_required': escalation_required,
                    'sla_compliance': {
                        'met': False,
                        'response_time_minutes': response_time_minutes,
                        'target_time_minutes': target_time_minutes
                    },
                    'next_actions': []
                },
                'payload_generated': True,
                'generation_timestamp': current_time.isoformat(),
                'error': str(e)
            }
    
    def extract_entities(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Extract entities from customer request (delegated from Atlas)"""
        logger.info("        🔍 Extracting entities")
        
        request_text = state.get('request', {}).get('description', '')
        
        # Simple entity extraction
        entities = {
            'urgency_level': 'high' if any(word in request_text.lower() for word in ['urgent', 'critical', 'emergency']) else 'medium',
            'issue_type': 'technical' if any(word in request_text.lower() for word in ['api', 'error', 'timeout', 'integration']) else 'general',
            'product_mentions': [word for word in ['api', 'authentication', 'billing', 'account'] if word in request_text.lower()]
        }
        
        return {
            'extracted_entities': entities,
            'extraction_timestamp': datetime.now().isoformat()
        }
    
    def enrich_records(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich customer records with additional data (delegated from Atlas)"""
        logger.info("        📊 Enriching records")
        
        customer_id = state.get('customer_id')
        
        # Mock enrichment data
        enrichment = {
            'account_status': 'active',
            'support_tier': 'premium',
            'previous_issues': 2,
            'satisfaction_score': 4.5,
            'last_contact': '2024-01-10'
        }
        
        return {
            'enriched_data': enrichment,
            'enrichment_timestamp': datetime.now().isoformat()
        }
    
    def escalation_decision(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Make escalation decision based on analysis"""
        logger.info("        ⬆️ Making escalation decision")
        
        urgency = state.get('request', {}).get('urgency', 'medium')
        customer_tier = state.get('customer_context', {}).get('subscription_tier', 'basic')
        
        should_escalate = urgency == 'critical' or customer_tier == 'premium'
        
        return {
            'escalation_required': should_escalate,
            'escalation_reason': f"Urgency: {urgency}, Tier: {customer_tier}",
            'escalation_timestamp': datetime.now().isoformat()
        }
    
    def solution_evaluation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate potential solutions"""
        logger.info("        🎯 Evaluating solutions")
        
        issue_type = state.get('request', {}).get('category', 'general')
        
        solutions = {
            'technical_issue': ['Check API credentials', 'Verify endpoint configuration', 'Review error logs'],
            'billing_inquiry': ['Review account status', 'Check payment history', 'Update billing information'],
            'general': ['Provide documentation', 'Schedule consultation', 'Escalate to specialist']
        }
        
        recommended_solutions = solutions.get(issue_type, solutions['general'])
        
        return {
            'recommended_solutions': recommended_solutions,
            'solution_confidence': 0.85,
            'evaluation_timestamp': datetime.now().isoformat()
        }
    
    def update_payload(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Update the workflow payload with processed data"""
        logger.info("        🔄 Updating payload")
        
        # Update state with processed information
        updates = {
            'processing_complete': True,
            'last_updated': datetime.now().isoformat(),
            'workflow_stage': 'decision_complete'
        }
        
        return {
            'payload_updates': updates,
            'update_timestamp': datetime.now().isoformat()
        }

# Add the missing get_server function and server instance
common_server = CommonServerAbilities()

def get_server():
    """Get the Common MCP server instance."""
    return common_server

if __name__ == "__main__":
    # Test the server
    server = get_server()
    print(f"Common Server initialized")
    
    # Test a basic ability
    test_state = {"customer_id": "test123", "request": {"subject": "Test"}}
    result = server.accept_payload(test_state)
    print(f"Accept payload result: {result}")