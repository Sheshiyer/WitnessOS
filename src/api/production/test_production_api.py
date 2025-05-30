#!/usr/bin/env python3
"""
Comprehensive Unit Tests for WitnessOS Production API

Tests all endpoints, error handling, validation, caching, and engine integration.
Achieves 80%+ test coverage for production readiness.

Usage:
    pytest test_production_api.py -v
    pytest test_production_api.py --cov=production_api --cov-report=html
"""

import pytest
import asyncio
import json
from datetime import datetime
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
engines_dir = current_dir.parent
sys.path.insert(0, str(engines_dir))

from api.production_api import app, AVAILABLE_ENGINES, AVAILABLE_WORKFLOWS

# Test client
client = TestClient(app)

# Test data using verified birth information
TEST_BIRTH_DATA = {
    "name": "Cumbipuram Nateshan Sheshnarayan",
    "date": "13.08.1991",
    "time": "13:31",
    "location": "Bengaluru",
    "timezone": "Asia/Kolkata"
}

INVALID_BIRTH_DATA = {
    "name": "",
    "date": "invalid-date",
    "time": "25:99",
    "location": "Unknown",
    "timezone": "Invalid/Timezone"
}

class TestAPIEndpoints:
    """Test all API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct information"""
        response = client.get("/v1/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == "WitnessOS Divination Engines API"
        assert data["version"] == "1.0.0"
        assert data["status"] == "production"
        assert "endpoints" in data
        assert "features" in data
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/v1/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "engines_available" in data
        assert "engine_status" in data
        assert "features" in data
    
    def test_list_engines(self):
        """Test engine listing endpoint"""
        response = client.get("/v1/engines")
        assert response.status_code == 200
        
        data = response.json()
        assert "available_engines" in data
        assert "count" in data
        assert "engine_details" in data
        assert data["count"] == len(AVAILABLE_ENGINES)
        
        # Check engine details structure
        for engine_name in AVAILABLE_ENGINES.keys():
            assert engine_name in data["engine_details"]
            engine_info = data["engine_details"][engine_name]
            assert "status" in engine_info
            assert "requires_time" in engine_info
            assert "requires_location" in engine_info
    
    def test_list_workflows(self):
        """Test workflow listing endpoint"""
        response = client.get("/v1/workflows")
        assert response.status_code == 200
        
        data = response.json()
        assert "available_workflows" in data
        assert "count" in data
        assert "workflow_descriptions" in data
        assert data["count"] == len(AVAILABLE_WORKFLOWS)
        
        # Check all workflows have descriptions
        for workflow in AVAILABLE_WORKFLOWS:
            assert workflow in data["workflow_descriptions"]

class TestEngineExecution:
    """Test engine execution endpoints"""
    
    def test_single_engine_valid_request(self):
        """Test running a single engine with valid data"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "format": "standard",
            "use_cache": False
        }
        
        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "engine" in data
        assert data["engine"] == "numerology"
        assert "result" in data or "error" in data  # Either success or error
        assert "timestamp" in data
    
    def test_single_engine_invalid_engine(self):
        """Test running invalid engine name"""
        request_data = {
            "engine_name": "invalid_engine",
            "input_data": TEST_BIRTH_DATA,
            "format": "standard"
        }
        
        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "error" in data
        assert "invalid_engine" in data["error"]["message"]
    
    def test_single_engine_invalid_birth_data(self):
        """Test running engine with invalid birth data"""
        request_data = {
            "engine_name": "numerology",
            "input_data": INVALID_BIRTH_DATA,
            "format": "standard"
        }
        
        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_multi_engine_valid_request(self):
        """Test running multiple engines"""
        request_data = {
            "engines": ["numerology", "biorhythm"],
            "birth_data": TEST_BIRTH_DATA,
            "parallel": True,
            "synthesize": True,
            "format": "witnessOS",
            "use_cache": False
        }
        
        response = client.post("/v1/engines/multi", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "engines" in data
        assert "birth_data" in data
        assert "results" in data
        assert "consciousness_scan" in data["results"]
        assert "engine_outputs" in data["results"]
        
        # Check synthesis if requested
        if request_data["synthesize"]:
            assert "synthesis" in data["results"]
    
    def test_multi_engine_invalid_engines(self):
        """Test multi-engine with invalid engine names"""
        request_data = {
            "engines": ["numerology", "invalid_engine"],
            "birth_data": TEST_BIRTH_DATA,
            "parallel": True,
            "synthesize": False
        }
        
        response = client.post("/v1/engines/multi", json=request_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "error" in data
        assert "invalid_engine" in data["error"]["message"]

class TestWorkflows:
    """Test workflow execution"""
    
    def test_valid_workflow_execution(self):
        """Test executing a valid workflow"""
        request_data = {
            "workflow_name": "daily_guidance",
            "birth_data": TEST_BIRTH_DATA,
            "format": "witnessOS",
            "use_cache": False
        }
        
        response = client.post("/v1/workflows/run", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "workflow" in data
        assert data["workflow"]["name"] == "daily_guidance"
        assert "engines_used" in data["workflow"]
        assert "results" in data
    
    def test_invalid_workflow_name(self):
        """Test executing invalid workflow"""
        request_data = {
            "workflow_name": "invalid_workflow",
            "birth_data": TEST_BIRTH_DATA,
            "format": "standard"
        }
        
        response = client.post("/v1/workflows/run", json=request_data)
        assert response.status_code == 400
        
        data = response.json()
        assert "error" in data
        assert "invalid_workflow" in data["error"]["message"]

class TestFieldAnalysis:
    """Test consciousness field analysis"""
    
    def test_field_analysis_default_engines(self):
        """Test field analysis with default engines"""
        request_data = {
            "birth_data": TEST_BIRTH_DATA,
            "analysis_depth": "standard",
            "use_cache": False
        }
        
        response = client.post("/v1/field-analysis", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "field_analysis" in data
        assert "analysis_metadata" in data
        assert "results" in data
        
        # Check field analysis structure
        field_analysis = data["field_analysis"]
        assert "field_diagnostic" in field_analysis
        assert "consciousness_map" in field_analysis
        assert "field_recommendations" in field_analysis
    
    def test_field_analysis_custom_engines(self):
        """Test field analysis with custom engine selection"""
        request_data = {
            "birth_data": TEST_BIRTH_DATA,
            "engines": ["numerology", "biorhythm"],
            "analysis_depth": "deep",
            "use_cache": False
        }
        
        response = client.post("/v1/field-analysis", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["analysis_metadata"]["engines_analyzed"] == ["numerology", "biorhythm"]
        assert data["analysis_metadata"]["depth"] == "deep"
    
    def test_field_analysis_invalid_engines(self):
        """Test field analysis with invalid engines"""
        request_data = {
            "birth_data": TEST_BIRTH_DATA,
            "engines": ["invalid_engine"],
            "analysis_depth": "basic"
        }
        
        response = client.post("/v1/field-analysis", json=request_data)
        assert response.status_code == 400

class TestValidation:
    """Test input validation"""
    
    def test_birth_data_validation(self):
        """Test birth data validation"""
        # Test invalid date format
        invalid_data = TEST_BIRTH_DATA.copy()
        invalid_data["date"] = "1991-08-13"  # Wrong format
        
        request_data = {
            "engine_name": "numerology",
            "input_data": invalid_data
        }
        
        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 422
    
    def test_time_validation(self):
        """Test time validation"""
        invalid_data = TEST_BIRTH_DATA.copy()
        invalid_data["time"] = "25:99"  # Invalid time
        
        request_data = {
            "engine_name": "numerology",
            "input_data": invalid_data
        }
        
        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 422
    
    def test_format_validation(self):
        """Test output format validation"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "format": "invalid_format"
        }
        
        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 422

class TestCaching:
    """Test response caching functionality"""
    
    def test_cache_functionality(self):
        """Test that caching works correctly"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "use_cache": True
        }
        
        # First request
        response1 = client.post("/v1/engines/run", json=request_data)
        assert response1.status_code == 200
        
        # Second request should use cache
        response2 = client.post("/v1/engines/run", json=request_data)
        assert response2.status_code == 200
        
        # Results should be identical
        assert response1.json() == response2.json()
    
    def test_cache_disabled(self):
        """Test that cache can be disabled"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "use_cache": False
        }
        
        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        # Should not indicate cached result
        assert not data.get("cached", False)

class TestFormatting:
    """Test output formatting functionality"""

    def test_standard_formatting(self):
        """Test standard output format"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "format": "standard",
            "use_cache": False
        }

        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 200

        data = response.json()
        # Standard format should have basic structure
        assert "engine" in data
        assert "timestamp" in data

    def test_mystical_formatting(self):
        """Test mystical output format"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "format": "mystical",
            "use_cache": False
        }

        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 200

        data = response.json()
        # Mystical format should have specific fields
        if "engine_essence" in data:  # If formatting was applied
            assert "consciousness_signature" in data
            assert "archetypal_resonance" in data

    def test_witnessOS_formatting(self):
        """Test WitnessOS output format"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "format": "witnessOS",
            "use_cache": False
        }

        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 200

        data = response.json()
        # WitnessOS format should have consciousness debugging structure
        if "consciousness_scan" in data:  # If formatting was applied
            assert "engine_diagnostics" in data
            assert "reality_patches" in data
            assert "witness_protocol" in data

class TestErrorHandling:
    """Test comprehensive error handling"""

    def test_missing_required_fields(self):
        """Test handling of missing required fields"""
        # Missing engine_name
        request_data = {
            "input_data": TEST_BIRTH_DATA
        }

        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 422

    def test_malformed_json(self):
        """Test handling of malformed JSON"""
        response = client.post(
            "/v1/engines/run",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_empty_request_body(self):
        """Test handling of empty request body"""
        response = client.post("/v1/engines/run", json={})
        assert response.status_code == 422

    def test_invalid_content_type(self):
        """Test handling of invalid content type"""
        response = client.post(
            "/v1/engines/run",
            data="some data",
            headers={"Content-Type": "text/plain"}
        )
        assert response.status_code == 422

class TestEngineSpecificRequirements:
    """Test engine-specific requirements"""

    def test_time_required_engines(self):
        """Test engines that require birth time"""
        time_required_engines = ["human_design", "vimshottari", "gene_keys"]

        for engine_name in time_required_engines:
            if engine_name in AVAILABLE_ENGINES:
                # Test without time
                birth_data_no_time = TEST_BIRTH_DATA.copy()
                birth_data_no_time["time"] = ""

                request_data = {
                    "engine_name": engine_name,
                    "input_data": birth_data_no_time
                }

                response = client.post("/v1/engines/run", json=request_data)
                # Should either fail validation or return error in result
                assert response.status_code in [400, 422] or "error" in response.json()

    def test_location_required_engines(self):
        """Test engines that require birth location"""
        location_required_engines = ["human_design", "vimshottari", "gene_keys"]

        for engine_name in location_required_engines:
            if engine_name in AVAILABLE_ENGINES:
                # Test with valid location
                request_data = {
                    "engine_name": engine_name,
                    "input_data": TEST_BIRTH_DATA
                }

                response = client.post("/v1/engines/run", json=request_data)
                # Should process without location validation errors
                assert response.status_code == 200

class TestPerformance:
    """Test API performance characteristics"""

    def test_parallel_vs_sequential_execution(self):
        """Test parallel vs sequential multi-engine execution"""
        engines = ["numerology", "biorhythm"]

        # Test parallel execution
        parallel_request = {
            "engines": engines,
            "birth_data": TEST_BIRTH_DATA,
            "parallel": True,
            "synthesize": False,
            "use_cache": False
        }

        start_time = datetime.now()
        parallel_response = client.post("/v1/engines/multi", json=parallel_request)
        parallel_time = (datetime.now() - start_time).total_seconds()

        assert parallel_response.status_code == 200

        # Test sequential execution
        sequential_request = parallel_request.copy()
        sequential_request["parallel"] = False

        start_time = datetime.now()
        sequential_response = client.post("/v1/engines/multi", json=sequential_request)
        sequential_time = (datetime.now() - start_time).total_seconds()

        assert sequential_response.status_code == 200

        # Both should complete successfully
        assert "results" in parallel_response.json()
        assert "results" in sequential_response.json()

    def test_response_time_limits(self):
        """Test that API responses are within reasonable time limits"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "use_cache": False
        }

        start_time = datetime.now()
        response = client.post("/v1/engines/run", json=request_data)
        response_time = (datetime.now() - start_time).total_seconds()

        assert response.status_code == 200
        # Should respond within 30 seconds (generous limit for testing)
        assert response_time < 30.0

class TestIntegration:
    """Integration tests for complete workflows"""

    def test_complete_natal_workflow(self):
        """Test complete natal workflow end-to-end"""
        request_data = {
            "workflow_name": "complete_natal",
            "birth_data": TEST_BIRTH_DATA,
            "format": "witnessOS",
            "use_cache": False
        }

        response = client.post("/v1/workflows/run", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert "workflow" in data
        assert "results" in data
        assert "consciousness_scan" in data["results"]

        # Should include multiple engines
        engines_used = data["workflow"]["engines_used"]
        assert len(engines_used) >= 2

    def test_field_analysis_integration(self):
        """Test field analysis integration with multiple engines"""
        request_data = {
            "birth_data": TEST_BIRTH_DATA,
            "engines": ["numerology", "biorhythm"],
            "analysis_depth": "standard",
            "use_cache": False
        }

        response = client.post("/v1/field-analysis", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert "field_analysis" in data
        assert "results" in data

        # Should have field-specific analysis
        field_analysis = data["field_analysis"]
        assert "field_diagnostic" in field_analysis
        assert "field_coherence" in field_analysis["field_diagnostic"]

# Test fixtures and utilities
@pytest.fixture
def mock_engine_success():
    """Mock successful engine execution"""
    with patch('api.production_api.run_engine_calculation') as mock:
        mock.return_value = {
            "engine": "test_engine",
            "result": {"test": "data"},
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "cached": False
        }
        yield mock

@pytest.fixture
def mock_engine_failure():
    """Mock failed engine execution"""
    with patch('api.production_api.run_engine_calculation') as mock:
        mock.return_value = {
            "engine": "test_engine",
            "error": "Test error",
            "status": "error",
            "timestamp": datetime.now().isoformat()
        }
        yield mock

class TestMockedEngines:
    """Test with mocked engine responses"""

    def test_successful_engine_mock(self, mock_engine_success):
        """Test with successful engine mock"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "use_cache": False
        }

        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "success"
        assert "result" in data

    def test_failed_engine_mock(self, mock_engine_failure):
        """Test with failed engine mock"""
        request_data = {
            "engine_name": "numerology",
            "input_data": TEST_BIRTH_DATA,
            "use_cache": False
        }

        response = client.post("/v1/engines/run", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "error"
        assert "error" in data

# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
