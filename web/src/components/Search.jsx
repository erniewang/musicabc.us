import { createRef, useEffect, useState } from 'react';
import {
  Box,
  Center,
  Input,
  InputGroup,
  InputLeftAddon,
  InputRightElement,
} from '@chakra-ui/react';
import { FaRegTimesCircle } from 'react-icons/fa';

const Search = ({ setAbc }) => {
  const [term, setTerm] = useState({
    text: '',
    suggestions: [],
  });
  const [choices, setChoices] = useState([]);
  const thisInput = createRef();

  useEffect(() => {
    setTerm((prev) => ({
      ...prev,
      suggestions: choices,
    }))
  },[choices]);

  const maybeSetChoices = (json) => {
    if (Array.isArray(json)) {
      setChoices(json);
    }
  };

  const onChange = (e) => {
    const value = e.target.value;
    if (value.length > 1) {
      fetch(`/api/search/${value}`)
        .then((res) => res.json())
        .then((json) => maybeSetChoices(json))
        .then((err) => console.log(err)); 
    }
    setTerm({
      text: value,
      suggestions: [],
    })
  };
  
  const maybeSetAbc = (json) => {
    if (json?.abc) {
      setAbc(json.abc);
    }
  };
  
  const suggestionSelected = (suggestion) => {
    setTerm({
      text: suggestion.title,
      suggestions: [],
    })
    fetch(`/api/get/${suggestion.id}`)
      .then((res) => res.json())
      .then((json) => maybeSetAbc(json))
      .then((err) => console.log(err)); 
  };
  
  const showSuggestions = () => {
   if (term.suggestions.length === 0) {
     return null;
   }
   return (
     <ul>
       {term.suggestions.map((s) => (
         <li
           key={s.id}
           onClick={(e)=>suggestionSelected(s)}
         >
           {s.title}
         </li>)
       )}
     </ul>
   )
  };
  
  const clearInput = () => {
    setTerm({ text: '', suggestions: []});
    thisInput.current.focus();
  };

  return (
      <Center>
        <Box w='50%' className="tadd">
          <InputGroup m='3' >
            <InputLeftAddon
              children="Search ABC"
              fontFamily="Oswald"
            />
            <Input
              ref={thisInput}
              autoFocus
              variant='outline'
              placeholder='start typing name of music'
              value={term.text}
              onChange={onChange}
            />
            <InputRightElement
              children={<FaRegTimesCircle />}
              onClick={clearInput}
            />
          </InputGroup>
          { showSuggestions() }
        </Box>
      </Center>
  );
};

export default Search;
