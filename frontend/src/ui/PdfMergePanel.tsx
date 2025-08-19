import React from 'react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';

export const PdfMergePanel: React.FC = () => {
  const [files, setFiles] = React.useState<FileList | null>(null);

  const merge = useMutation({
    mutationFn: async (data: FormData) => {
      const res = await axios.post('http://127.0.0.1:8000/merge_pdfs', data, {responseType:'blob'});
      return res.data as Blob;
    }
  });

  const onSubmit = () => {
    if (!files || files.length === 0) return;
    const fd = new FormData();
    for (const f of Array.from(files)) fd.append('files', f);
    fd.append('output_name', 'merged_web.pdf');
    merge.mutate(fd);
  };

  return (
    <div style={{minWidth:340, padding:'1rem', border:'1px solid #ddd', borderRadius:8}}>
      <h2 style={{marginTop:0}}>PDF Merge</h2>
      <input type="file" multiple accept="application/pdf" onChange={e=>setFiles(e.target.files)} />
      <button style={{display:'block', marginTop:8}} disabled={!files || merge.isPending} onClick={onSubmit}>
        {merge.isPending ? 'Merging...' : 'Merge PDFs'}
      </button>
      {merge.isSuccess && (
        <p style={{fontSize:12, color:'green'}}>Merged {files?.length} file(s). (Browser will allow download automatically soon.)</p>
      )}
      {merge.isError && <p style={{color:'red', fontSize:12}}>Error merging PDFs</p>}
    </div>
  );
};
