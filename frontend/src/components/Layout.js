import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Home, Users, FileText, History, LogOut } from 'lucide-react';

export const Sidebar = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard', roles: ['all'] },
    { path: '/employees', icon: Users, label: 'Colaboradores', roles: ['all'] },
    { path: '/measures', icon: FileText, label: 'Medidas', roles: ['all'] },
    { path: '/measures/acknowledge', icon: FileText, label: 'Receber Medidas', roles: ['colaborador'] },
    { path: '/hierarchy', icon: Users, label: 'Hierarquia', roles: ['gerente', 'coordenador', 'supervisor'] },
    { path: '/documents', icon: FileText, label: 'Documentos', roles: ['rh', 'gerente', 'coordenador', 'supervisor'] },
  ];

  if (user?.role === 'juridico' || user?.role === 'rh') {
    menuItems.push({ path: '/audit', icon: History, label: 'Auditoria', roles: ['juridico', 'rh'] });
  }

  const filteredMenuItems = menuItems.filter(item => {
    if (item.roles.includes('all')) return true;
    return item.roles.includes(user?.role);
  });

  const filteredMenuItems = menuItems.filter(item => {
    if (item.roles.includes('all')) return true;
    return item.roles.includes(user?.role);
  });

  return (
    <div className="sidebar" data-testid="sidebar">
      <div className="p-6 border-b border-white/10">
        <h1 className="text-2xl font-bold">Bússola</h1>
        <p className="text-white/70 text-sm mt-1">{user?.name}</p>
        <p className="text-white/50 text-xs mt-0.5 capitalize">{user?.role}</p>
      </div>

      <nav className="flex-1 p-4 space-y-2">
        {filteredMenuItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <Link
              key={item.path}
              to={item.path}
              data-testid={`nav-${item.path.slice(1)}`}
            >
              <div
                className={`flex items-center gap-3 px-4 py-3 rounded-md transition-colors ${
                  isActive
                    ? 'bg-white/10 text-white font-medium'
                    : 'text-white/70 hover:bg-white/5 hover:text-white'
                }`}
              >
                <Icon className="h-5 w-5" />
                <span>{item.label}</span>
              </div>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/10">
        <Button
          onClick={logout}
          variant="ghost"
          className="w-full justify-start text-white/70 hover:text-white hover:bg-white/5"
          data-testid="logout-button"
        >
          <LogOut className="h-5 w-5 mr-3" />
          Sair
        </Button>
      </div>
    </div>
  );
};

export const MainLayout = ({ children }) => {
  return (
    <div className="App">
      <Sidebar />
      <div className="main-content">
        <div className="p-8">
          {children}
        </div>
      </div>
    </div>
  );
};
