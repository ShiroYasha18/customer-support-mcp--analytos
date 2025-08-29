"""
🌍 **ATLAS MCP Server** (external-facing abilities)

Simulates external system integrations for customer support workflow.
Handles abilities that interact with outside systems like APIs, databases, and third-party services.

Responsibilities:
- Entity extraction from customer messages
- Record enrichment with external data
- Knowledge base search
- Ticket system updates
- External API calls
- Customer notifications

How to extend:
- Add more "external integration" abilities here
- For now, mock them with static/dummy values
- In a real system, replace mocks with API/database calls
"""

import json
import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class AtlasServer:
    """ATLAS MCP Server - External system integrations"""
    
    def __init__(self):
        self.name = "atlas"
        self.description = "External system integrations and API calls"
        logger.info(f"Initialized {self.name} server")
    
    def get_abilities(self) -> List[str]:
        """Return list of available external abilities"""
        return [
            "extract_entities",
            "enrich_records", 
            "clarify_question",
            "extract_answer",
            "store_answer",
            "knowledge_base_search",
            "store_data",
            "escalation_decision",
            "solution_evaluation",
            "update_payload",
            "update_ticket",
            "close_ticket",
            "execute_api_calls",
            "trigger_notifications",
            # Legacy abilities (keeping for backward compatibility)
            "analyze_sentiment",
            "detect_language",
            "fetch_interaction_history",
            "get_account_details",
            "rank_solutions",
            "filter_by_relevance",
            "format_final_response",
            "schedule_followup"
        ]
    
    def execute_ability(self, ability_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an external ability with given context"""
        logger.info(f"Executing external ability: {ability_name}")
        
        ability_map = {
            # New LangGraph spec abilities
            "enrich_records": self._enrich_records,
            "clarify_question": self._clarify_question,
            "extract_answer": self._extract_answer,
            "store_answer": self._store_answer,
            "knowledge_base_search": self._knowledge_base_search,
            "store_data": self._store_data,
            "escalation_decision": self._escalation_decision,
            "solution_evaluation": self._solution_evaluation,
            "update_payload": self._update_payload,
            "update_ticket": self._update_ticket,
            "close_ticket": self._close_ticket,
            "execute_api_calls": self._execute_api_calls,
            "trigger_notifications": self._trigger_notifications,
            # Legacy abilities
            "extract_entities": self._extract_entities,
            "enrich_customer_record": self._enrich_customer_record,
            "search_knowledge_base": self._search_knowledge_base,
            "update_ticket_system": self._update_ticket_system,
            "call_external_api": self._call_external_api,
            "send_notification": self._send_notification,
            "escalate_to_human": self._escalate_to_human,
            "update_crm_system": self._update_crm_system,
            "check_service_status": self._check_service_status,
            "log_interaction": self._log_interaction,
            "generate_case_id": self._generate_case_id,
            "analyze_sentiment": self._analyze_sentiment,
            "detect_language": self._detect_language,
            "fetch_interaction_history": self._fetch_interaction_history,
            "get_account_details": self._get_account_details,
            "rank_solutions": self._rank_solutions,
            "filter_by_relevance": self._filter_by_relevance,
            "format_final_response": self._format_final_response,
            "schedule_followup": self._schedule_followup
        }
        
        if ability_name in ability_map:
            result = ability_map[ability_name](context)
            logger.info(f"External ability {ability_name} completed successfully")
            return result
        else:
            error_msg = f"Unknown external ability: {ability_name}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    # New LangGraph spec abilities
    def _enrich_records(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich customer records with external data sources."""
        customer_id = context.get("customer_id", "unknown")
        
        # Mock external data enrichment
        enriched_data = {
            "customer_segment": "enterprise",
            "lifetime_value": 50000,
            "support_tier": "premium",
            "previous_escalations": 2,
            "satisfaction_score": 4.2,
            "preferred_contact_method": "email",
            "timezone": "UTC-5",
            "account_manager": "Sarah Johnson"
        }
        
        return {
            "enrichment_success": True,
            "enriched_data": enriched_data,
            "data_sources": ["CRM", "Support_History", "Billing_System"],
            "enrichment_timestamp": datetime.now().isoformat()
        }
    
    def _clarify_question(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate clarifying questions when needed."""
        query = context.get("query", "")
        category = context.get("request_category", "general_inquiry")
        
        # Generate contextual clarifying questions
        clarifying_questions = {
            "billing": [
                "What specific billing period are you asking about?",
                "Are you referring to a particular charge or the entire invoice?"
            ],
            "technical_issue": [
                "What error message are you seeing?",
                "When did this issue first occur?",
                "What steps have you already tried?"
            ],
            "account_access": [
                "Are you unable to log in or having trouble with specific features?",
                "What happens when you try to access your account?"
            ]
        }
        
        questions = clarifying_questions.get(category, [
            "Could you provide more details about your request?",
            "What specific outcome are you looking for?"
        ])
        
        return {
            "clarification_needed": len(query.split()) < 10,  # Simple heuristic
            "suggested_questions": questions,
            "question_category": category,
            "clarification_timestamp": datetime.now().isoformat()
        }
    
    def _extract_answer(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract customer answers from follow-up responses."""
        response_text = context.get("customer_response", "")
        
        # Mock answer extraction
        extracted_info = {
            "key_points": response_text.split(".")[:3],  # First 3 sentences
            "sentiment": "neutral",
            "urgency_level": "medium",
            "contains_new_info": len(response_text) > 50
        }
        
        return {
            "extraction_success": True,
            "extracted_answer": extracted_info,
            "extraction_confidence": 0.8,
            "extraction_timestamp": datetime.now().isoformat()
        }
    
    def _store_answer(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Store customer answers in the system."""
        answer_data = context.get("extracted_answer", {})
        case_id = context.get("case_id", "unknown")
        
        # Mock storage operation
        storage_result = {
            "stored_successfully": True,
            "storage_location": f"case_answers/{case_id}",
            "answer_id": f"ans_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "storage_timestamp": datetime.now().isoformat()
        }
        
        return {
            "storage_result": storage_result,
            "answer_stored": True,
            "storage_timestamp": datetime.now().isoformat()
        }
    
    def _knowledge_base_search(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search knowledge base for relevant solutions."""
        query = context.get("query", "")
        category = context.get("request_category", "general_inquiry")
        
        # Mock knowledge base results
        kb_results = [
            {
                "id": "kb_001",
                "title": "How to reset your password",
                "relevance": 0.95,
                "category": "account_access",
                "solution_steps": ["Click forgot password", "Check email", "Follow link"]
            },
            {
                "id": "kb_002", 
                "title": "Billing inquiry resolution",
                "relevance": 0.87,
                "category": "billing",
                "solution_steps": ["Review invoice", "Contact billing team", "Request adjustment"]
            }
        ]
        
        # Filter by category
        filtered_results = [r for r in kb_results if r["category"] == category][:3]
        
        return {
            "search_success": True,
            "knowledge_base_results": filtered_results,
            "total_results": len(filtered_results),
            "search_timestamp": datetime.now().isoformat()
        }
    
    def _store_data(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Store processed data in external systems."""
        data_to_store = context.get("processed_data", {})
        
        # Mock data storage
        storage_operations = [
            {"system": "data_warehouse", "status": "success", "record_id": "dw_12345"},
            {"system": "analytics_db", "status": "success", "record_id": "an_67890"},
            {"system": "backup_storage", "status": "success", "record_id": "bk_54321"}
        ]
        
        return {
            "storage_operations": storage_operations,
            "all_successful": all(op["status"] == "success" for op in storage_operations),
            "storage_timestamp": datetime.now().isoformat()
        }
    
    def _escalation_decision(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Make escalation decision based on context analysis."""
        logger.info("        🔺 Making escalation decision")
        
        # Analyze escalation factors
        priority = context.get('priority', 'medium')
        complexity = context.get('complexity', 'medium')
        customer_tier = context.get('customer_tier', 'standard')
        previous_escalations = context.get('previous_escalations', 0)
        
        escalation_score = 0
        
        # Priority factor
        if priority == 'high': escalation_score += 30
        elif priority == 'medium': escalation_score += 10
        
        # Complexity factor
        if complexity == 'high': escalation_score += 25
        elif complexity == 'medium': escalation_score += 10
        
        # Customer tier factor
        if customer_tier == 'premium': escalation_score += 20
        elif customer_tier == 'enterprise': escalation_score += 30
        
        # Previous escalations factor
        escalation_score += min(previous_escalations * 15, 45)
        
        escalate = escalation_score >= 50
        
        return {
            "escalation_decision": escalate,
            "escalation_score": escalation_score,
            "escalation_reason": "High complexity and priority" if escalate else "Standard resolution path",
            "recommended_tier": "specialist" if escalation_score >= 70 else "senior_agent" if escalate else "standard_agent"
        }
    
    def _solution_evaluation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate potential solutions and rank them by effectiveness."""
        logger.info("        🎯 Evaluating solutions")
        
        solutions = context.get('solutions', [])
        customer_context = context.get('customer_context', {})
        issue_type = context.get('issue_type', 'general')
        
        if not solutions:
            # Generate default solutions based on issue type
            if issue_type == 'account_access':
                solutions = [
                    {'id': 1, 'description': 'Password reset via email', 'complexity': 'low'},
                    {'id': 2, 'description': 'Account verification and manual unlock', 'complexity': 'medium'},
                    {'id': 3, 'description': 'Security team investigation', 'complexity': 'high'}
                ]
            elif issue_type == 'billing':
                solutions = [
                    {'id': 1, 'description': 'Review billing statement and explain charges', 'complexity': 'low'},
                    {'id': 2, 'description': 'Process refund or credit adjustment', 'complexity': 'medium'},
                    {'id': 3, 'description': 'Escalate to billing specialist', 'complexity': 'high'}
                ]
            else:
                solutions = [
                    {'id': 1, 'description': 'Provide standard troubleshooting steps', 'complexity': 'low'},
                    {'id': 2, 'description': 'Schedule technical consultation', 'complexity': 'medium'},
                    {'id': 3, 'description': 'Escalate to technical team', 'complexity': 'high'}
                ]
        
        # Evaluate each solution
        evaluated_solutions = []
        for solution in solutions:
            effectiveness_score = 70  # Base score
            
            # Adjust based on complexity and customer tier
            complexity = solution.get('complexity', 'medium')
            customer_tier = customer_context.get('tier', 'standard')
            
            if complexity == 'low':
                effectiveness_score += 20
            elif complexity == 'high':
                effectiveness_score -= 10
            
            if customer_tier == 'premium':
                effectiveness_score += 10
            elif customer_tier == 'enterprise':
                effectiveness_score += 15
            
            evaluated_solutions.append({
                **solution,
                'effectiveness_score': min(effectiveness_score, 100),
                'estimated_resolution_time': self._estimate_resolution_time(complexity),
                'customer_satisfaction_impact': 'high' if effectiveness_score >= 80 else 'medium' if effectiveness_score >= 60 else 'low'
            })
        
        # Sort by effectiveness score
        evaluated_solutions.sort(key=lambda x: x['effectiveness_score'], reverse=True)
        
        return {
            'solution_evaluation': {
                'total_solutions': len(evaluated_solutions),
                'recommended_solution': evaluated_solutions[0] if evaluated_solutions else None,
                'all_solutions': evaluated_solutions,
                'evaluation_criteria': ['effectiveness', 'complexity', 'customer_tier', 'resolution_time']
            },
            'evaluation_timestamp': datetime.now().isoformat()
        }
    
    def _estimate_resolution_time(self, complexity: str) -> str:
        """Estimate resolution time based on complexity."""
        time_estimates = {
            'low': '15-30 minutes',
            'medium': '1-2 hours', 
            'high': '4-8 hours'
        }
        return time_estimates.get(complexity, '1-2 hours')
    
    def _update_payload(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Update the workflow payload with new information."""
        updates = context.get("payload_updates", {})
        
        # Mock payload update
        updated_fields = list(updates.keys()) if updates else ["status", "last_modified"]
        
        return {
            "payload_updated": True,
            "updated_fields": updated_fields,
            "update_count": len(updated_fields),
            "update_timestamp": datetime.now().isoformat()
        }
    
    def _update_ticket(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Update ticket in external ticketing system."""
        ticket_id = context.get("ticket_id", "unknown")
        updates = context.get("ticket_updates", {})
        
        # Mock ticket update
        return {
            "ticket_update_success": True,
            "ticket_id": ticket_id,
            "updated_fields": list(updates.keys()) if updates else ["status", "resolution"],
            "update_timestamp": datetime.now().isoformat()
        }
    
    def _close_ticket(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Close ticket in external system."""
        ticket_id = context.get("ticket_id", "unknown")
        resolution = context.get("resolution", "Resolved by automated system")
        
        return {
            "ticket_closed": True,
            "ticket_id": ticket_id,
            "resolution": resolution,
            "closure_timestamp": datetime.now().isoformat()
        }
    
    def _execute_api_calls(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute external API calls."""
        api_calls = context.get("api_calls", [])
        
        # Mock API execution
        results = []
        for call in api_calls:
            results.append({
                "api": call.get("name", "unknown"),
                "status": "success",
                "response_code": 200,
                "execution_time_ms": 150
            })
        
        return {
            "api_execution_results": results,
            "all_successful": all(r["status"] == "success" for r in results),
            "total_calls": len(results),
            "execution_timestamp": datetime.now().isoformat()
        }
    
    def _trigger_notifications(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger customer notifications."""
        notification_types = context.get("notification_types", ["email"])
        customer = context.get("customer", {})
        
        # Mock notification triggering
        notifications_sent = []
        for notification_type in notification_types:
            notifications_sent.append({
                "type": notification_type,
                "recipient": customer.get("email", "unknown@example.com"),
                "status": "sent",
                "message_id": f"msg_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            })
        
        return {
            "notifications_triggered": True,
            "notifications_sent": notifications_sent,
            "total_notifications": len(notifications_sent),
            "trigger_timestamp": datetime.now().isoformat()
        }

    def _extract_entities(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract entities from customer message (mock implementation)"""
        message = context.get("customer_message", "")
        
        # Mock entity extraction - in real system, use NLP service
        entities = {
            "customer_id": "CUST_12345",
            "product_mentioned": "Premium Plan" if "premium" in message.lower() else "Basic Plan",
            "issue_type": "billing" if any(word in message.lower() for word in ["bill", "charge", "payment"]) else "technical",
            "urgency": "high" if any(word in message.lower() for word in ["urgent", "asap", "emergency"]) else "medium",
            "sentiment": "negative" if any(word in message.lower() for word in ["angry", "frustrated", "disappointed"]) else "neutral"
        }
        
        return {
            "success": True,
            "entities": entities,
            "confidence_score": 0.85
        }
    
    def _enrich_customer_record(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich customer record with external data (mock implementation)"""
        customer_id = context.get("customer_id", "unknown")
        
        # Mock customer enrichment - in real system, query CRM/database
        enriched_data = {
            "customer_tier": "Premium",
            "account_status": "Active",
            "last_interaction": "2024-01-15",
            "total_tickets": 3,
            "satisfaction_score": 4.2,
            "preferred_contact": "email",
            "timezone": "UTC-8",
            "language": "English"
        }
        
        return {
            "success": True,
            "customer_data": enriched_data,
            "data_source": "CRM_API"
        }
    
    def _search_knowledge_base(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search knowledge base for relevant articles (mock implementation)"""
        query = context.get("search_query", "")
        
        # Mock KB search - in real system, use search API
        articles = [
            {
                "id": "KB_001",
                "title": "How to Reset Your Password",
                "relevance_score": 0.92,
                "url": "https://help.company.com/password-reset"
            },
            {
                "id": "KB_002", 
                "title": "Billing FAQ",
                "relevance_score": 0.78,
                "url": "https://help.company.com/billing-faq"
            }
        ]
        
        return {
            "success": True,
            "articles": articles,
            "total_results": len(articles)
        }
    
    def _update_ticket_system(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Update external ticket system (mock implementation)"""
        ticket_data = context.get("ticket_data", {})
        
        # Mock ticket update - in real system, call ticketing API
        ticket_id = f"TKT_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "success": True,
            "ticket_id": ticket_id,
            "status": "created",
            "priority": ticket_data.get("priority", "medium")
        }
    
    def _call_external_api(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Make external API call (mock implementation)"""
        api_endpoint = context.get("endpoint", "unknown")
        
        # Mock API call - in real system, make HTTP request
        return {
            "success": True,
            "api_response": {"status": "ok", "data": "mock_response"},
            "endpoint": api_endpoint,
            "response_time_ms": 150
        }
    
    def _send_notification(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Send notification to customer (mock implementation)"""
        notification_type = context.get("type", "email")
        recipient = context.get("recipient", "customer@example.com")
        
        # Mock notification - in real system, use notification service
        return {
            "success": True,
            "notification_id": f"NOTIF_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "type": notification_type,
            "recipient": recipient,
            "status": "sent"
        }
    
    def _escalate_to_human(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Escalate case to human agent (mock implementation)"""
        escalation_reason = context.get("reason", "complex_issue")
        
        # Mock escalation - in real system, route to agent queue
        return {
            "success": True,
            "escalation_id": f"ESC_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "assigned_agent": "Agent_Sarah_M",
            "queue_position": 2,
            "estimated_wait_time": "5-10 minutes"
        }
    
    def _update_crm_system(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Update CRM system with interaction data (mock implementation)"""
        customer_id = context.get("customer_id", "unknown")
        
        # Mock CRM update - in real system, call CRM API
        return {
            "success": True,
            "crm_record_id": f"CRM_{customer_id}_{datetime.now().strftime('%Y%m%d')}",
            "updated_fields": ["last_contact", "interaction_count", "case_history"],
            "sync_status": "completed"
        }
    
    def _check_service_status(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check external service status (mock implementation)"""
        service_name = context.get("service", "main_platform")
        
        # Mock service check - in real system, ping service endpoints
        return {
            "success": True,
            "service": service_name,
            "status": "operational",
            "uptime": "99.9%",
            "last_incident": "2024-01-10"
        }
    
    def _log_interaction(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Log interaction to external analytics system (mock implementation)"""
        interaction_data = context.get("interaction", {})
        
        # Mock logging - in real system, send to analytics platform
        return {
            "success": True,
            "log_id": f"LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "logged_at": datetime.now().isoformat(),
            "analytics_system": "DataWarehouse_v2"
        }
    
    def _generate_case_id(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate unique case ID (mock implementation)"""
        customer_id = context.get("customer_id", "UNKNOWN")
        
        # Mock case ID generation - in real system, use ID service
        case_id = f"CASE_{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "success": True,
            "case_id": case_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": "2024-12-31T23:59:59"
        }

    def _analyze_sentiment(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze sentiment of customer message (mock implementation)"""
        message = context.get("message", "")
        
        # Mock sentiment analysis - in real system, use NLP service
        negative_words = ["angry", "frustrated", "disappointed", "terrible", "awful", "hate"]
        positive_words = ["great", "excellent", "love", "amazing", "wonderful", "perfect"]
        
        message_lower = message.lower()
        negative_count = sum(1 for word in negative_words if word in message_lower)
        positive_count = sum(1 for word in positive_words if word in message_lower)
        
        if negative_count > positive_count:
            sentiment = "negative"
            confidence = min(0.9, 0.6 + (negative_count * 0.1))
        elif positive_count > negative_count:
            sentiment = "positive"
            confidence = min(0.9, 0.6 + (positive_count * 0.1))
        else:
            sentiment = "neutral"
            confidence = 0.7
        
        return {
            "success": True,
            "sentiment": sentiment,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }

    def _detect_language(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Detect language of customer message (mock implementation)"""
        message = context.get("message", "")
        
        # Mock language detection - in real system, use language detection service
        # Simple heuristic based on common words
        spanish_words = ["hola", "gracias", "por favor", "ayuda", "problema"]
        french_words = ["bonjour", "merci", "s'il vous plaît", "aide", "problème"]
        
        message_lower = message.lower()
        spanish_count = sum(1 for word in spanish_words if word in message_lower)
        french_count = sum(1 for word in french_words if word in message_lower)
        
        if spanish_count > 0:
            language = "es"
            confidence = 0.85
        elif french_count > 0:
            language = "fr"
            confidence = 0.85
        else:
            language = "en"
            confidence = 0.9
        
        return {
            "success": True,
            "language": language,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }

    def _fetch_interaction_history(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch customer interaction history (mock implementation)"""
        customer_id = context.get("customer_id", "unknown")
        
        # Mock interaction history - in real system, query database
        interactions = [
            {
                "id": "INT_001",
                "date": "2024-01-15T10:30:00Z",
                "type": "chat",
                "summary": "Password reset request",
                "resolution": "resolved"
            },
            {
                "id": "INT_002",
                "date": "2024-01-10T14:20:00Z",
                "type": "email",
                "summary": "Billing inquiry",
                "resolution": "resolved"
            },
            {
                "id": "INT_003",
                "date": "2024-01-05T09:15:00Z",
                "type": "phone",
                "summary": "Technical support",
                "resolution": "escalated"
            }
        ]
        
        return {
            "success": True,
            "customer_id": customer_id,
            "interactions": interactions,
            "total_count": len(interactions),
            "timestamp": datetime.now().isoformat()
        }

    def _get_account_details(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get customer account details (mock implementation)"""
        customer_id = context.get("customer_id", "unknown")
        
        # Mock account details - in real system, query customer database
        account_details = {
            "customer_id": customer_id,
            "account_type": "Premium",
            "status": "Active",
            "created_date": "2023-06-15",
            "last_login": "2024-01-16T08:30:00Z",
            "subscription_expires": "2024-12-31",
            "payment_method": "Credit Card (**** 1234)",
            "support_tier": "Priority",
            "contact_preferences": ["email", "sms"]
        }
        
        return {
            "success": True,
            "account_details": account_details,
            "timestamp": datetime.now().isoformat()
        }

    def _rank_solutions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Rank potential solutions by relevance (mock implementation)"""
        solutions = context.get("solutions", [])
        query = context.get("query", "")
        
        # Mock solution ranking - in real system, use ML ranking model
        ranked_solutions = []
        for i, solution in enumerate(solutions):
            # Simple scoring based on keyword matching
            score = 0.8 - (i * 0.1)  # Decreasing score
            ranked_solutions.append({
                "solution": solution,
                "relevance_score": max(0.1, score),
                "rank": i + 1
            })
        
        return {
            "success": True,
            "ranked_solutions": ranked_solutions,
            "total_solutions": len(ranked_solutions),
            "timestamp": datetime.now().isoformat()
        }

    def _filter_by_relevance(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Filter content by relevance threshold (mock implementation)"""
        items = context.get("items", [])
        threshold = context.get("threshold", 0.5)
        
        # Mock relevance filtering - in real system, use ML filtering
        filtered_items = []
        for item in items:
            # Assign mock relevance score
            relevance_score = 0.7  # Mock score
            if relevance_score >= threshold:
                filtered_items.append({
                    "item": item,
                    "relevance_score": relevance_score
                })
        
        return {
            "success": True,
            "filtered_items": filtered_items,
            "original_count": len(items),
            "filtered_count": len(filtered_items),
            "threshold": threshold,
            "timestamp": datetime.now().isoformat()
        }

    def _format_final_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Format final response for customer (mock implementation)"""
        response_data = context.get("response_data", {})
        customer_language = context.get("language", "en")
        
        # Mock response formatting - in real system, use templating engine
        formatted_response = {
            "greeting": "Thank you for contacting us!",
            "main_content": response_data.get("content", "We have processed your request."),
            "next_steps": "Please let us know if you need further assistance.",
            "contact_info": "You can reach us at support@company.com",
            "case_reference": response_data.get("case_id", "N/A")
        }
        
        return {
            "success": True,
            "formatted_response": formatted_response,
            "language": customer_language,
            "timestamp": datetime.now().isoformat()
        }

    def _schedule_followup(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule follow-up with customer (mock implementation)"""
        customer_id = context.get("customer_id", "unknown")
        followup_type = context.get("type", "email")
        delay_hours = context.get("delay_hours", 24)
        
        # Mock follow-up scheduling - in real system, use scheduling service
        from datetime import timedelta
        scheduled_time = datetime.now() + timedelta(hours=delay_hours)
        
        return {
            "success": True,
            "followup_id": f"FU_{customer_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "customer_id": customer_id,
            "type": followup_type,
            "scheduled_time": scheduled_time.isoformat(),
            "status": "scheduled",
            "timestamp": datetime.now().isoformat()
        }

# Create server instance
atlas_server = AtlasServer()

def get_server():
    """Get the ATLAS server instance"""
    return atlas_server

if __name__ == "__main__":
    # Test the server
    server = get_server()
    print(f"ATLAS Server initialized with abilities: {server.get_abilities()}")
    
    # Test entity extraction
    test_context = {"customer_message": "I'm having urgent billing issues with my premium account"}
    result = server.execute_ability("extract_entities", test_context)
    print(f"Entity extraction result: {json.dumps(result, indent=2)}")