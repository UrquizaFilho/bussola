import React, { useState, useEffect } from 'react';
import { MainLayout } from '../components/Layout';
import { documentApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { FileText, Download, Upload } from 'lucide-react';
import { toast } from 'sonner';

export default function DocumentsPage() {
  const { user } = useAuth();
  const [templates, setTemplates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [measureType, setMeasureType] = useState('');

  const isRH = user?.role === 'rh';

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    try {
      const response = await documentApi.getTemplates();
      setTemplates(response.data);
    } catch (error) {
      console.error('Erro ao carregar templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && (file.name.endsWith('.doc') || file.name.endsWith('.docx'))) {
      setSelectedFile(file);
    } else {
      toast.error('Apenas arquivos Word (.doc, .docx) são permitidos');
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      toast.error('Selecione um arquivo');
      return;
    }

    setUploading(true);
    try {
      await documentApi.uploadTemplate(selectedFile, measureType);
      toast.success('Template enviado com sucesso!');
      setSelectedFile(null);
      setMeasureType('');
      loadTemplates();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Erro ao enviar template');
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async (templateId, filename) => {
    try {
      const response = await documentApi.downloadTemplate(templateId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('Download iniciado');
    } catch (error) {
      toast.error('Erro ao baixar template');
    }
  };

  if (loading) {
    return (
      <MainLayout>
        <div className="text-center py-12">Carregando...</div>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div className="space-y-6" data-testid="documents-page">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Documentos e Templates</h1>
          <p className="text-slate-600 mt-1">Gerencie templates de medidas disciplinares</p>
        </div>

        {isRH && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5" />
                Upload de Template
              </CardTitle>
              <CardDescription>
                Envie templates Word para serem usados nas medidas disciplinares
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleUpload} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="file">Arquivo Word (.doc, .docx) *</Label>
                  <Input
                    id="file"
                    type="file"
                    accept=".doc,.docx"
                    onChange={handleFileSelect}
                    data-testid="file-input"
                    className="h-10"
                  />
                  {selectedFile && (
                    <p className="text-sm text-slate-600">Arquivo selecionado: {selectedFile.name}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="measure_type">Tipo de Medida (Opcional)</Label>
                  <Select value={measureType} onValueChange={setMeasureType}>
                    <SelectTrigger className="h-10">
                      <SelectValue placeholder="Selecione o tipo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="advertencia_verbal">Advertência Verbal</SelectItem>
                      <SelectItem value="advertencia_escrita">Advertência Escrita</SelectItem>
                      <SelectItem value="suspensao">Suspensão</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <Button
                  type="submit"
                  disabled={!selectedFile || uploading}
                  className="bg-[#1B2A4E] hover:bg-[#1B2A4E]/90"
                  data-testid="upload-button"
                >
                  <Upload className="h-4 w-4 mr-2" />
                  {uploading ? 'Enviando...' : 'Enviar Template'}
                </Button>
              </form>
            </CardContent>
          </Card>
        )}

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Templates Disponíveis
            </CardTitle>
            <CardDescription>
              {templates.length} template(s) cadastrado(s)
            </CardDescription>
          </CardHeader>
          <CardContent>
            {templates.length === 0 ? (
              <p className="text-slate-500 text-center py-8">Nenhum template disponível</p>
            ) : (
              <div className="space-y-2">
                {templates.map((template) => (
                  <div
                    key={template.id}
                    className="flex items-center justify-between p-4 bg-slate-50 rounded-lg hover:bg-slate-100 transition-colors"
                    data-testid={`template-${template.id}`}
                  >
                    <div className="flex items-center gap-3">
                      <FileText className="h-8 w-8 text-[#1B2A4E]" />
                      <div>
                        <p className="font-medium text-slate-900">{template.name}</p>
                        {template.measure_type && (
                          <p className="text-sm text-slate-600 capitalize">
                            {template.measure_type.replace('_', ' ')}
                          </p>
                        )}
                        <p className="text-xs text-slate-500">
                          Enviado por {template.uploaded_by_name}
                        </p>
                      </div>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDownload(template.id, template.name)}
                      data-testid={`download-${template.id}`}
                    >
                      <Download className="h-4 w-4 mr-2" />
                      Baixar
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  );
}
