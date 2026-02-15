import requests
import sys
import json
from datetime import datetime

class BussolaAPITester:
    def __init__(self, base_url="https://medidas-tracker.preview.emergentagent.com/api"):
        self.base_url = base_url
        self.token = None
        self.tests_run = 0
        self.tests_passed = 0
        self.employee_id = None
        self.measure_id = None

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = requests.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = requests.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
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

    def test_login(self, email, password):
        """Test login and get token"""
        success, response = self.run_test(
            f"Login ({email})",
            "POST",
            "auth/login",
            200,
            data={"email": email, "password": password}
        )
        if success and 'token' in response:
            self.token = response['token']
            print(f"   Token obtained: {self.token[:20]}...")
            return True
        return False

    def test_auth_me(self):
        """Test get current user info"""
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        return success, response

    def test_create_employee(self):
        """Create a test employee"""
        employee_data = {
            "name": "João Silva",
            "cpf": "123.456.789-00",
            "department": "TI",
            "position": "Desenvolvedor",
            "admission_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        success, response = self.run_test(
            "Create Employee",
            "POST",
            "employees/",
            201,
            data=employee_data
        )
        
        if success and 'id' in response:
            self.employee_id = response['id']
            print(f"   Employee ID: {self.employee_id}")
        
        return success, response

    def test_get_employees(self):
        """Get all employees"""
        success, response = self.run_test(
            "Get Employees",
            "GET",
            "employees/",
            200
        )
        return success, response

    def test_get_employee_detail(self):
        """Get employee details"""
        if not self.employee_id:
            print("❌ No employee ID available for detail test")
            return False, {}
            
        success, response = self.run_test(
            "Get Employee Detail",
            "GET",
            f"employees/{self.employee_id}",
            200
        )
        return success, response

    def test_create_measure(self):
        """Create a disciplinary measure"""
        if not self.employee_id:
            print("❌ No employee ID available for measure creation")
            return False, {}
            
        measure_data = {
            "employee_id": self.employee_id,
            "type": "advertencia",
            "reason": "Atraso reincorrente",
            "description": "Colaborador apresentou atrasos em 3 dias consecutivos"
        }
        
        success, response = self.run_test(
            "Create Measure",
            "POST",
            "measures/",
            201,
            data=measure_data
        )
        
        if success and 'id' in response:
            self.measure_id = response['id']
            print(f"   Measure ID: {self.measure_id}")
        
        return success, response

    def test_get_measures(self):
        """Get all measures"""
        success, response = self.run_test(
            "Get Measures",
            "GET",
            "measures/",
            200
        )
        return success, response

    def test_sign_measure(self):
        """Sign a measure (Jurídico/RH only)"""
        if not self.measure_id:
            print("❌ No measure ID available for signing")
            return False, {}
            
        success, response = self.run_test(
            "Sign Measure",
            "POST",
            f"measures/{self.measure_id}/sign",
            200
        )
        return success, response

    def test_dashboard_stats(self):
        """Get dashboard statistics"""
        success, response = self.run_test(
            "Dashboard Stats",
            "GET",
            "measures/dashboard/stats",
            200
        )
        return success, response

    def test_audit_logs(self):
        """Get audit logs"""
        success, response = self.run_test(
            "Audit Logs",
            "GET",
            "audit/logs",
            200
        )
        return success, response

def main():
    print("🚀 Starting Bússola API Tests")
    print("=" * 50)
    
    tester = BussolaAPITester()
    
    # Test credentials from the request
    test_accounts = [
        {"email": "rh@bussola.com", "password": "senha123", "role": "RH"},
        {"email": "juridico@bussola.com", "password": "senha123", "role": "Jurídico"},
        {"email": "gestor@bussola.com", "password": "senha123", "role": "Gestor"}
    ]
    
    for account in test_accounts:
        print(f"\n{'='*20} Testing with {account['role']} Account {'='*20}")
        
        # Login
        if not tester.test_login(account['email'], account['password']):
            print(f"❌ Login failed for {account['role']}, skipping tests")
            continue
        
        # Test auth/me
        tester.test_auth_me()
        
        # Test dashboard stats
        tester.test_dashboard_stats()
        
        # Test employees endpoints
        tester.test_get_employees()
        
        # Create employee (only for RH account to avoid duplicates)
        if account['role'] == 'RH':
            tester.test_create_employee()
            if tester.employee_id:
                tester.test_get_employee_detail()
                
                # Create measure
                tester.test_create_measure()
                
                # Test measures
                tester.test_get_measures()
        
        # Test signing (only for RH/Jurídico)
        if account['role'] in ['RH', 'Jurídico'] and tester.measure_id:
            tester.test_sign_measure()
        
        # Test audit (only for RH/Jurídico)
        if account['role'] in ['RH', 'Jurídico']:
            tester.test_audit_logs()
        
        print(f"\n📊 {account['role']} Tests: {tester.tests_passed}/{tester.tests_run} passed")
    
    print(f"\n{'='*50}")
    print(f"🏁 Final Results: {tester.tests_passed}/{tester.tests_run} tests passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed - check logs above")
        return 1

if __name__ == "__main__":
    sys.exit(main())