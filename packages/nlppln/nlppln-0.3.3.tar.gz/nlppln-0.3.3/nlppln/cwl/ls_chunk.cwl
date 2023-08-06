#!/usr/bin/env cwlrunner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "-m", "nlppln.commands.ls_chunk"]

stdout: cwl.output.json

inputs:
  in_dir:
    type: Directory
    inputBinding:
      position: 1
  chunks:
    type: File
    inputBinding:
      position: 2
  name:
    type: string?
    inputBinding:
      prefix: --name

outputs:
  out_files:
    type: File[]
