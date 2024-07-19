---
layout: ../layouts/BaseLayout.astro
---

# Changelog

# toc

# Changelog

> Changelog for [ALab](https://animallogic.com/alab/).

### 2.2.0

- Split main package in two: 
  - `asset_structure`: Available as well as a GitHub repository to facilitate external experimentation and collaboration on the asset structure.
  - `techvar_assets`: Geometry, lights, shaders, rigs which are the heavy assets containing artistic contributions. 

### 2.1.0

- Updated geometry proxies to more closely match the **render** `purpose` geometry.
- Global `entities` of `component` `Kind` have textures for `cards` Draw Mode.
- Adjustments to global `entities` to allow broadcasting changes without destroying `instancing` via an `inherits` `arc`.
- All `exr` textures now correctly mipmapped.
- All `entities` now have extent hints.
- Use of `inherits` `composition arc`.
- Fixed issue where whiskers on **stoat01** were disappearing when FX caches were turned on.
- Removed unused metadata from texture files.
- Opacity textures in shaders are no longer used for non-transparent objects.
- Up axis metadata is properly set to the valid token "Y".

### 2.0.1

- Removed unexpected **\_\_MACOSX** artifact from the zip file.
- Removed non-required exr texture metadata.
- Mipmapped textures, which were not mipmapped.
- All geo `fragments` have **extentsHint** `property`.
- Modified Stoat's sweater material roughness on `baked_procedurals` package.

### 2.0.0

- Added full production shot example with two animated characters.
- Extended ALab set to include over 300 fully surfaced assets.
- All the geo with render `purpose` utilizes two UV sets:
  - **primvars:perfuv** - Simplified UVs used for **preview** material binding.
  - **primvars:st** - UDIM-based UVs used for **full** material binding.
- UsdPreviewSurface Materials are now bound to the geometry using the **UsdShade.Tokens.full** and **UsdShade.Tokens.preview** `purposes`.
- Low-res textures are now 1K Multi-UDIM Exrs.
- Inclusion of Render Procedurals such as **Weave** and **Alfro** as baked curves.
- Character and Prop Animation data is stored under **geocache** `fragments`. The animation is represented through the time-sampled `attributes` in USD, including extent, normals, points, orientation, scale, and translation.
- Added **CharFxCaches** from charFX simulations, resolving collision on dynamics (e.g. between cloth and skin).
