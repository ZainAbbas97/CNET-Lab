import { create } from 'zustand'

interface Dataset {
  rows: number
  columns: string[]
  shape: [number, number]
}

interface Store {
  sessionId: string | null
  dataset: Dataset | null
  plotData: any | null
  output: string[]
  setSessionId: (id: string) => void
  setDataset: (dataset: Dataset) => void
  setPlotData: (data: any) => void
  addOutput: (text: string) => void
  clearOutput: () => void
}

export const useStore = create<Store>((set) => ({
  sessionId: null,
  dataset: null,
  plotData: null,
  output: [],
  setSessionId: (id) => set({ sessionId: id }),
  setDataset: (dataset) => set({ dataset }),
  setPlotData: (data) => set({ plotData: data }),
  addOutput: (text) => set((state) => ({ output: [...state.output, text] })),
  clearOutput: () => set({ output: [] }),
}))

