import React from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { Toaster } from "@/components/ui/sonner";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import EmployeesPage from "./pages/EmployeesPage";
import NewEmployeePage from "./pages/NewEmployeePage";
import EmployeeDetailPage from "./pages/EmployeeDetailPage";
import MeasuresPage from "./pages/MeasuresPage";
import NewMeasurePage from "./pages/NewMeasurePage";
import AcknowledgeMeasurePage from "./pages/AcknowledgeMeasurePage";
import WitnessAcknowledgePage from "./pages/WitnessAcknowledgePage";
import HierarchyPage from "./pages/HierarchyPage";
import DocumentsPage from "./pages/DocumentsPage";
import UsersManagementPage from "./pages/UsersManagementPage";
import AuditPage from "./pages/AuditPage";

const PrivateRoute = ({ children }) => {
  const { token, loading } = useAuth();

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Carregando...</div>;
  }

  return token ? children : <Navigate to="/login" />;
};

function AppRoutes() {
  const { token } = useAuth();

  return (
    <Routes>
      <Route path="/login" element={token ? <Navigate to="/dashboard" /> : <LoginPage />} />
      <Route
        path="/dashboard"
        element={
          <PrivateRoute>
            <DashboardPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/employees"
        element={
          <PrivateRoute>
            <EmployeesPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/employees/new"
        element={
          <PrivateRoute>
            <NewEmployeePage />
          </PrivateRoute>
        }
      />
      <Route
        path="/employees/:id"
        element={
          <PrivateRoute>
            <EmployeeDetailPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/measures"
        element={
          <PrivateRoute>
            <MeasuresPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/measures/new"
        element={
          <PrivateRoute>
            <NewMeasurePage />
          </PrivateRoute>
        }
      />
      <Route
        path="/measures/acknowledge"
        element={
          <PrivateRoute>
            <AcknowledgeMeasurePage />
          </PrivateRoute>
        }
      />
      <Route
        path="/measures/acknowledge-witnesses"
        element={
          <PrivateRoute>
            <WitnessAcknowledgePage />
          </PrivateRoute>
        }
      />
      <Route
        path="/hierarchy"
        element={
          <PrivateRoute>
            <HierarchyPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/documents"
        element={
          <PrivateRoute>
            <DocumentsPage />
          </PrivateRoute>
        }
      />
      <Route
        path="/audit"
        element={
          <PrivateRoute>
            <AuditPage />
          </PrivateRoute>
        }
      />
      <Route path="/" element={<Navigate to="/dashboard" />} />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
        <Toaster position="top-right" />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
