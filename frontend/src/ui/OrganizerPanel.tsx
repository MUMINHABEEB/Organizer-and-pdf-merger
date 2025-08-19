import React from 'react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

interface OrganizePayload {
  base_directory: string;
  dry_run: boolean;
  scheme: string;
}

export const OrganizerPanel: React.FC = () => {
  const [dir, setDir] = React.useState('');
  const [dryRun, setDryRun] = React.useState(true);
  const [scheme, setScheme] = React.useState('standard');

  const organize = useMutation({
    mutationFn: async (payload: OrganizePayload) => {
      const res = await axios.post('http://127.0.0.1:8000/organize', payload);
      return res.data;
    }
  });

  return (
    <div style={{minWidth:340, padding:'1rem', border:'1px solid #ddd', borderRadius:8}}>
      <h2 style={{marginTop:0}}>Organizer</h2>
      <label style={{display:'block', marginBottom:8}}>
        Base Directory
        <input style={{width:'100%', marginTop:4}} value={dir} onChange={e=>setDir(e.target.value)} placeholder="C:/path/to/folder" />
      </label>
      <label style={{display:'flex', alignItems:'center', gap:6, marginBottom:8}}>
        <input type="checkbox" checked={dryRun} onChange={e=>setDryRun(e.target.checked)} /> Dry Run
      </label>
      <label style={{display:'block', marginBottom:8}}>
        Scheme
        <select style={{width:'100%', marginTop:4}} value={scheme} onChange={e=>setScheme(e.target.value)}>
          <option value="standard">standard</option>
          <option value="sample">sample</option>
        </select>
      </label>
      <button disabled={!dir || organize.isPending} onClick={()=>organize.mutate({base_directory:dir, dry_run:dryRun, scheme})}>
        {organize.isPending ? 'Running...' : 'Organize'}
      </button>
      {organize.isError && <p style={{color:'red'}}>Error: {(organize.error as any).message}</p>}
      {organize.isSuccess && (
        <div style={{marginTop:12, fontSize:12}}>
          <strong>Result:</strong>
          <pre style={{maxHeight:160, overflow:'auto', background:'#f7f7f7', padding:8}}>{JSON.stringify(organize.data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};
