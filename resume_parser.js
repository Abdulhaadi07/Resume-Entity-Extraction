import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Upload } from 'lucide-react';
import * as genai from 'google.generativeai'; // Importing Gemini

// Configuring Gemini
genai.configure(api_key="AIzaSyAp7j1icQOWFH-b6ZZ1E-uqfHYd50q9ZoA");
const model = genai.GenerativeModel("gemini-1.5-flash");

const ResumeParser = () => {
  const navigate = useNavigate();
  const [resumeContent, setResumeContent] = useState('');
  const [parsedResume, setParsedResume] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState('');

  // Function to handle file upload
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    try {
      const text = await readFileContent(file);
      setResumeContent(text);
      setError('');
    } catch (err) {
      setError('Error reading file. Please try again.');
      console.error('File reading error:', err);
    }
  };

  // Function to read file content
  const readFileContent = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (event) => resolve(event.target.result);
      reader.onerror = (error) => reject(error);
      reader.readAsText(file);
    });
  };

  // Function to process resume through Gemini
  const processResume = async () => {
    if (!resumeContent.trim()) {
      setError('Please enter or upload resume content.');
      return;
    }

    setIsProcessing(true);
    setError('');

    try {
      const prompt = `
        Parse the following resume content. Please:
        1. Normalize all abbreviations and standardize terms
        2. Analyze context for repeated terms
        3. Structure the content into clear sections

        Resume content:
        ${resumeContent}
      `;

      // Calling Gemini API
      const response = await model.generate_content(prompt);
      const parsedContent = JSON.parse(response.text); // Assuming the response text is JSON string

      setParsedResume(parsedContent);

      // Redirect to the parsed result page
      navigate('/parsed', { state: { parsedResume: parsedContent } });

    } catch (err) {
      setError('Error processing resume. Please try again.');
      console.error('Processing error:', err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto">
      <CardHeader>
        <CardTitle>Resume Parser</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="upload" className="space-y-4">
          <TabsList>
            <TabsTrigger value="upload">Upload Resume</TabsTrigger>
            <TabsTrigger value="manual">Manual Input</TabsTrigger>
          </TabsList>

          <TabsContent value="upload" className="space-y-4">
            <div className="flex items-center justify-center w-full">
              <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer hover:bg-gray-50">
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <Upload className="w-8 h-8 mb-4 text-gray-500" />
                  <p className="mb-2 text-sm text-gray-500">
                    <span className="font-semibold">Click to upload</span> or drag and drop
                  </p>
                </div>
                <input
                  type="file"
                  className="hidden"
                  accept=".txt,.doc,.docx,.pdf"
                  onChange={handleFileUpload}
                />
              </label>
            </div>
          </TabsContent>

          <TabsContent value="manual" className="space-y-4">
            <Textarea 
              placeholder="Paste your resume content here..."
              value={resumeContent}
              onChange={(e) => setResumeContent(e.target.value)}
              className="min-h-[200px]"
            />
          </TabsContent>

          {error && <p className="text-red-500 text-sm">{error}</p>}

          <Button 
            onClick={processResume} 
            disabled={isProcessing || !resumeContent.trim()}
            className="w-full"
          >
            {isProcessing ? 'Processing...' : 'Parse Resume'}
          </Button>
        </Tabs>
      </CardContent>
    </Card>
  );
};

export default ResumeParser;
