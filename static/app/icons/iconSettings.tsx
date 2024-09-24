import {forwardRef} from 'react';

import type {SVGIconProps} from './svgIcon';
import {SvgIcon} from './svgIcon';

const IconSettings = forwardRef<SVGSVGElement, SVGIconProps>((props, ref) => {
  return (
    <SvgIcon {...props} ref={ref}>
      <path d="M8,10.73A2.73,2.73,0,1,1,10.73,8,2.74,2.74,0,0,1,8,10.73Zm0-4A1.23,1.23,0,1,0,9.23,8,1.23,1.23,0,0,0,8,6.77Z" />
      <path d="M8.05,16A2.07,2.07,0,0,1,6,13.93a.35.35,0,0,0-.22-.35.37.37,0,0,0-.41.05,2.07,2.07,0,0,1-1.5.64h0a2,2,0,0,1-1.43-.58l0,0a2.07,2.07,0,0,1,0-2.93.37.37,0,0,0,.1-.41.35.35,0,0,0-.31-.21H2.07A2.07,2.07,0,0,1,2.07,6a.35.35,0,0,0,.35-.22.37.37,0,0,0,0-.41,2.07,2.07,0,0,1-.64-1.5,2,2,0,0,1,.58-1.43l0,0a2.07,2.07,0,0,1,2.93,0,.37.37,0,0,0,.41.1l.13,0a.37.37,0,0,0,.13-.27V2.07a2.07,2.07,0,0,1,4.14,0,.36.36,0,0,0,.2.36.35.35,0,0,0,.38-.06,2.07,2.07,0,0,1,1.5-.64h0a2,2,0,0,1,1.43.58l0,0a2.07,2.07,0,0,1,0,2.93.37.37,0,0,0-.1.41.5.5,0,0,1,0,.13.37.37,0,0,0,.27.13h.11a2.07,2.07,0,0,1,0,4.14.36.36,0,0,0-.36.2h0a.36.36,0,0,0,.07.37,2.07,2.07,0,0,1,.64,1.5,2,2,0,0,1-.58,1.43l0,0a2.07,2.07,0,0,1-2.93,0,.37.37,0,0,0-.41-.1.35.35,0,0,0-.21.31v.11A2.07,2.07,0,0,1,8.05,16ZM5.59,12a1.83,1.83,0,0,1,.73.15,1.81,1.81,0,0,1,1.16,1.66.59.59,0,0,0,.57.65.56.56,0,0,0,.57-.57v-.11a1.84,1.84,0,0,1,3.13-1.31.6.6,0,0,0,.84.06l0,0a.56.56,0,0,0,0-.8,1.86,1.86,0,0,1-.41-2.07,1.84,1.84,0,0,1,1.68-1.11A.59.59,0,0,0,14.5,8a.57.57,0,0,0-.57-.57h-.11a1.84,1.84,0,0,1-1.69-1.11,1.33,1.33,0,0,1-.05-.19,1.82,1.82,0,0,1,.43-1.88.6.6,0,0,0,.06-.84l0,0a.56.56,0,0,0-.8,0,1.87,1.87,0,0,1-2.07.41A1.84,1.84,0,0,1,8.57,2.13.59.59,0,0,0,8,1.5a.57.57,0,0,0-.57.57v.11A1.84,1.84,0,0,1,6.32,3.87l-.19,0a1.8,1.8,0,0,1-1.88-.43.6.6,0,0,0-.84-.06l0,0a.56.56,0,0,0,0,.8,1.86,1.86,0,0,1,.41,2.07A1.81,1.81,0,0,1,2.15,7.48a.59.59,0,0,0-.65.57.56.56,0,0,0,.57.57h.11a1.84,1.84,0,0,1,1.31,3.13.6.6,0,0,0-.06.84l0,0a.56.56,0,0,0,.8,0A2,2,0,0,1,5.59,12ZM12.88,10h0Z" />
    </SvgIcon>
  );
});

IconSettings.displayName = 'IconSettings';

export {IconSettings};
