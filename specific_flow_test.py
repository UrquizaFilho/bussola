import requests
import sys
import json
from datetime import datetime

class SpecificFlowTester:
    def __init__(self, base_url="https://medidas-tracker.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.maria_id = None
        self.measure_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:300]}...")
                    return True, response_data
                except:
                    return True, {}
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   Error: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            return False, {}

    def test_rh_login(self):
        """Test RH login"""
        success, response = self.run_test(
            "RH Login",
            "POST",
            "auth/login",
            200,
            data={"email": "rh@bussola.com", "password": "senha123"}
        )
        if success and 'token' in response:
            self.token = response['token']
            print(f"   Token obtained: {self.token[:20]}...")
            return True
        return False

    def test_dashboard_stats(self):
        """Test dashboard statistics"""
        success, response = self.run_test(
            "Dashboard Statistics",
            "GET",
            "measures/dashboard/stats",
            200
        )
        if success:
            print(f"   📊 Dashboard Stats:")
            print(f"      Total Employees: {response.get('total_employees', 0)}")
            print(f"      Total Measures (Month): {response.get('total_measures_month', 0)}")
            print(f"      Pending Measures: {response.get('pending_measures', 0)}")
            print(f"      Advertências: {response.get('measures_by_type', {}).get('advertencia', 0)}")
            print(f"      Suspensões: {response.get('measures_by_type', {}).get('suspensao', 0)}")
        return success, response

    def test_create_maria_santos(self):
        """Create Maria Santos employee"""
        maria_data = {
            "name": "Maria Santos",
            "cpf": "987.654.321-00",
            "department": "Financeiro",
            "position": "Analista",
            "admission_date": "2024-01-15"
        }
        
        success, response = self.run_test(
            "Create Maria Santos",
            "POST",
            "employees/",
            200,  # API returns 200, not 201
            data=maria_data
        )
        
        if success and 'id' in response:
            self.maria_id = response['id']
            print(f"   Maria Santos ID: {self.maria_id}")
        
        return success, response

    def test_get_employees_list(self):
        """Get employees list to verify Maria Santos"""
        success, response = self.run_test(
            "Get Employees List",
            "GET",
            "employees/",
            200
        )
        
        if success and isinstance(response, list):
            maria_found = False
            for employee in response:
                if employee.get('name') == 'Maria Santos':
                    maria_found = True
                    self.maria_id = employee.get('id')  # Get Maria's ID from the list
                    print(f"   ✅ Maria Santos found in list:")
                    print(f"      ID: {self.maria_id}")
                    print(f"      Name: {employee.get('name')}")
                    print(f"      CPF: {employee.get('cpf')}")
                    print(f"      Department: {employee.get('department')}")
                    print(f"      Position: {employee.get('position')}")
                    break
            
            if not maria_found:
                print(f"   ❌ Maria Santos not found in employees list")
                
        return success, response

    def test_create_advertencia_measure(self):
        """Create Advertência measure for Maria Santos"""
        if not self.maria_id:
            print("❌ No Maria Santos ID available for measure creation")
            return False, {}
            
        measure_data = {
            "employee_id": self.maria_id,
            "type": "advertencia",
            "reason": "Falta não justificada",
            "description": "Colaboradora faltou ao trabalho sem apresentar justificativa adequada conforme política da empresa."
        }
        
        success, response = self.run_test(
            "Create Advertência Measure",
            "POST",
            "measures/",
            200,  # API might return 200 instead of 201
            data=measure_data
        )
        
        if success and 'id' in response:
            self.measure_id = response['id']
            print(f"   Measure ID: {self.measure_id}")
            print(f"   Status: {response.get('status', 'N/A')}")
        
        return success, response

    def test_get_measures_list(self):
        """Get measures list to verify the new measure"""
        success, response = self.run_test(
            "Get Measures List",
            "GET",
            "measures/",
            200
        )
        
        if success and isinstance(response, list):
            measure_found = False
            for measure in response:
                if measure.get('id') == self.measure_id:
                    measure_found = True
                    print(f"   ✅ Advertência measure found:")
                    print(f"      Type: {measure.get('type')}")
                    print(f"      Status: {measure.get('status')}")
                    print(f"      Reason: {measure.get('reason')}")
                    print(f"      Employee: {measure.get('employee_name', 'N/A')}")
                    break
            
            if not measure_found:
                print(f"   ❌ Created measure not found in measures list")
                
        return success, response

    def test_updated_dashboard_stats(self):
        """Test dashboard statistics after creating employee and measure"""
        success, response = self.run_test(
            "Updated Dashboard Statistics",
            "GET",
            "measures/dashboard/stats",
            200
        )
        if success:
            print(f"   📊 Updated Dashboard Stats:")
            print(f"      Total Employees: {response.get('total_employees', 0)}")
            print(f"      Total Measures (Month): {response.get('total_measures_month', 0)}")
            print(f"      Pending Measures: {response.get('pending_measures', 0)}")
            print(f"      Advertências: {response.get('measures_by_type', {}).get('advertencia', 0)}")
            print(f"      Suspensões: {response.get('measures_by_type', {}).get('suspensao', 0)}")
        return success, response

def main():
    print("🚀 Starting Specific Flow Test - Maria Santos")
    print("=" * 60)
    
    tester = SpecificFlowTester()
    
    # Step 1: Login with RH
    print(f"\n{'='*20} Step 1: RH Login {'='*20}")
    if not tester.test_rh_login():
        print("❌ RH Login failed, stopping tests")
        return 1
    
    # Step 2: Check initial dashboard stats
    print(f"\n{'='*20} Step 2: Initial Dashboard Stats {'='*20}")
    tester.test_dashboard_stats()
    
    # Step 3: Create Maria Santos
    print(f"\n{'='*20} Step 3: Create Maria Santos {'='*20}")
    tester.test_create_maria_santos()
    
    # Step 4: Verify Maria Santos in employees list
    print(f"\n{'='*20} Step 4: Verify Maria Santos in List {'='*20}")
    tester.test_get_employees_list()
    
    # Step 5: Create Advertência measure
    print(f"\n{'='*20} Step 5: Create Advertência Measure {'='*20}")
    tester.test_create_advertencia_measure()
    
    # Step 6: Verify measure in measures list
    print(f"\n{'='*20} Step 6: Verify Measure in List {'='*20}")
    tester.test_get_measures_list()
    
    # Step 7: Check updated dashboard stats
    print(f"\n{'='*20} Step 7: Updated Dashboard Stats {'='*20}")
    tester.test_updated_dashboard_stats()
    
    print(f"\n{'='*60}")
    print(f"🏁 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All specific flow tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed - check logs above")
        return 1

if __name__ == "__main__":
    sys.exit(main())