import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { AlertCircle } from 'lucide-react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(email, password);
    
    if (!result.success) {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div 
      className="auth-page" 
      style={{ backgroundImage: 'url(https://images.unsplash.com/photo-1713981910501-d68eca75eb32?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1MDV8MHwxfHNlYXJjaHwxfHxjb3Jwb3JhdGUlMjBvZmZpY2UlMjBhYnN0cmFjdCUyMGJhY2tncm91bmR8ZW58MHx8fHwxNzcxMTUwMTM1fDA&ixlib=rb-4.1.0&q=85)' }}
      data-testid="login-page"
    >
      <div className="relative z-10 w-full max-w-md px-6">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-[#1B2A4E] mb-2">Bússola</h1>
            <p className="text-slate-600">Sistema de Gestão de Medidas Disciplinares</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="seu@email.com"
                required
                data-testid="email-input"
                className="h-10"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Senha</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                data-testid="password-input"
                className="h-10"
              />
            </div>

            {error && (
              <div className="flex items-center gap-2 text-red-600 text-sm" data-testid="error-message">
                <AlertCircle className="h-4 w-4" />
                <span>{error}</span>
              </div>
            )}

            <Button
              type="submit"
              className="w-full bg-[#1B2A4E] hover:bg-[#1B2A4E]/90 text-white h-10"
              disabled={loading}
              data-testid="login-button"
            >
              {loading ? 'Entrando...' : 'Entrar'}
            </Button>
          </form>

          <div className="mt-6 p-4 bg-slate-50 rounded-md">
            <p className="text-xs text-slate-600 font-semibold mb-2">Contas Demo:</p>
            <div className="space-y-1 text-xs text-slate-600">
              <p>RH: rh@bussola.com / senha123</p>
              <p>Jurídico: juridico@bussola.com / senha123</p>
              <p>Gestor: gestor@bussola.com / senha123</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
