import React from 'react';
import { OrganizerPanel } from './OrganizerPanel';
import { PdfMergePanel } from './PdfMergePanel';

export const App: React.FC = () => {
  return (
    <div style={{fontFamily:'system-ui, sans-serif', margin:'1rem 2rem'}}>
      <h1>AI Automation Suite (Web)</h1>
      <p style={{opacity:.7}}>Prototype UI while migrating away from legacy desktop app.</p>
      <div style={{display:'flex', gap:'2rem', flexWrap:'wrap'}}>
        <OrganizerPanel />
        <PdfMergePanel />
      </div>
    </div>
  );
};
