import React, { useState } from 'react';

function ToggleText() {
  const [isVisible, setIsVisible] = useState(true);

  return (
    <div>
      <button onClick={() => setIsVisible(!isVisible)}>
        Toggle Text
      </button>
      {isVisible && <p>This text is toggleable</p>}
    </div>
  );
}

export default ToggleText;