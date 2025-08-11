import * as React from 'react';

export function TooltipProvider({ children }:{children:React.ReactNode}){ return <>{children}</>; }
export function Tooltip({ children }:{children:React.ReactNode}){ return <>{children}</>; }
export function TooltipTrigger({ children, ...props }:{children:React.ReactNode; className?:string}){ return <span {...props}>{children}</span>; }
export function TooltipContent({ children }:{children:React.ReactNode; className?:string}){ return <span>{children}</span>; }
