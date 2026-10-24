# Enclosure CAD status

`enclosure.py` is the parametric starting model for the team to inspect and revise. It does not claim PCB fit, snap-fit strength, acoustic performance, or print success. With CadQuery installed:

```sh
python3 hardware/cad/enclosure.py --help
python3 hardware/cad/enclosure.py --output hardware/cad/out
```

The generator produces native STEP/STL files only; PNG renders still require a CadQuery/FreeCAD rendering workflow and human inspection. `analytical_checks.py` provides a transparent `ESTIMATE` for snap-fit strain only; it is not a FEM result and is not included as measured evidence.
