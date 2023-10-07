// GlobalConfigContext.tsx
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { getConfig } from './configApi'; // 导入获取配置的函数

// 定义全局配置的接口
// 根据实际需要添加更多字段
export interface GlobalConfig {
  characterConfig?: {
    yourName: string;
    // 其他字段...
  };
  background_url: string;
  // 其他字段...
}

interface GlobalConfigContextProps {
  children: ReactNode;
}

const GlobalConfigContext = createContext<GlobalConfig | null>(null);

export function useGlobalConfig() {
  const context = useContext(GlobalConfigContext);
  if (!context) {
    throw new Error('useGlobalConfig must be used within a GlobalConfigProvider');
  }
  return context;
}

export function GlobalConfigProvider({ children }: GlobalConfigContextProps) {
  const [globalConfig, setGlobalConfig] = useState<GlobalConfig | null>(null);

  useEffect(() => {
    getConfig().then((data) => {
      setGlobalConfig(data);
    });
  }, []);

  return (
    <GlobalConfigContext.Provider value={globalConfig}>
      {children}
    </GlobalConfigContext.Provider>
  );
}
