import { useEffect, useState } from 'react';
import { Box, Grid, GridItem, Icon, Text } from '@chakra-ui/react'
import { FaArrowDown, FaArrowUp, FaUndo } from 'react-icons/fa';
import abcjs from 'abcjs';
import 'abcjs/abcjs-audio.css';


const AbcEditor = (props) => {
  const [abctxt, setAbctxt] = useState(props.abctxt);
  const [editor, setEditor] = useState(undefined);
  const [transposeLevel, setTransposeLevel] = useState(0);
  const [params, setParams] = useState({
    render: { selectTypes: false },
    synth: { }
  });

  const setupEditor = () => {
    setEditor(new abcjs.Editor('editor_abc', {
      canvas_id: 'paper_abc',
      warnings_id: 'warnings_abc',
      abcjsParams: { selectTypes: false },
      synth: {
        el: '#audio_abc',synth: { selectTypes: false },
        options: {
          displayRestart: true,
          displayPlay: true,
          displayProgress: true,
          options: {}
        }
      }
    }));
  };
  
  useEffect( () => {
    //abcjs.renderAbc('paper', tune, {});
    setupEditor(); 
  }, []);

  useEffect( () => {
    setAbctxt(props.abctxt);
    transposeReset();  // without this no re-render without click on textarea
  }, [props.abctxt]);

  useEffect( () => {
    if(!editor)return;
    editor.paramChanged(params.render);
    editor.synthParamChanged(params.synth);
  }, [params, editor]);

  const onAbcChange = (e) => {
    setAbctxt(e.target.value);
  };

  const transposeUp = () => {
    const newLevel = transposeLevel + 1;
    setTransposeLevel(newLevel);
    if(newLevel){
      setParams({
        render: { selectTypes: false, visualTranspose: newLevel},
        synth: { midiTranspose: newLevel }
      });
    } else {
      setParams({
        render: { selectTypes: false},
        synth: {}
      });
    }
  };

  const transposeDown = () => {
    const newLevel = transposeLevel - 1;
    setTransposeLevel(newLevel);
    setParams({
      render: { selectTypes: false, visualTranspose: newLevel},
      synth: { midiTranspose: newLevel }
    });
  };

  const transposeReset = () => {
    setTransposeLevel(0);
    setParams({
      render: { selectTypes: false, visualTranspose: 0},
      synth: { midiTranspose: 0 }
    });
  };

  return (
    <Grid
      templateColumns='repeat(3, 1fr)'
      gap={3}
    >
      <GridItem colSpan={1}>
	<div>
	  <p>ABC text:</p>
	  <textarea
	    id="editor_abc"
	    value={abctxt}
            cols={50}
            rows={15}
            wrap="soft"
            onChange={onAbcChange}
	  />
          <div id="warnings_abc"></div>
	  <Text fontSize='sm'color="red">
	    The text you highlighted will be shown in red in score.
	  </Text>
	</div>
        <div id="audio_abc"></div>
        <Box border='2px' borderColor='gray.200'>
	  <Text as='b'>Transpose</Text>
	  <br />
	  <span>current level: </span>
	  <Text as='mark'> {transposeLevel} </Text>
	  &nbsp; 
          <button onClick={transposeUp}><Icon as={FaArrowUp} /></button>
          <button onClick={transposeDown}><Icon as={FaArrowDown} /></button>
          <button onClick={transposeReset}><Icon as={FaUndo} /></button>
        </Box>
      </GridItem>
      <GridItem colSpan={2}>
        <div id="paper_abc" />
      </GridItem>
    </Grid>
  );
}

export default AbcEditor;