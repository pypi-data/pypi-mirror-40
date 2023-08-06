#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: cat

inputs:
  glob:
    type: File[]
    inputBinding:
      position: 0

stdout: out

outputs:
  concatenated:
    type: File
    outputBinding:
      glob: out
