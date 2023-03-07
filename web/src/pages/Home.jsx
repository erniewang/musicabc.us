import { useEffect, useState } from 'react';
import AbcEditor from '../components/AbcEditor';
import Search from '../components/Search';

const NoteEditor = () => {
  const [abctxt, setAbctxt] = useState('');
  useEffect(() => {
    console.log("setting abctxt from NoteEditor");
    console.log(abctxt);
  },[abctxt]);

  return (
    <div>
      <Search setAbc={setAbctxt}/>
      <AbcEditor abctxt={abctxt} />
    </div>
  );
}

export default NoteEditor;