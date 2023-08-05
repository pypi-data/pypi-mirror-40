#ifndef FASTNOISE_SIMD_WRAPPER_CPP
#define FASTNOISE_SIMD_WRAPPER_CPP

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION

#include <Python.h>
#include <numpy/npy_common.h>
#include <numpy/ndarrayobject.h>
#include <numpy/arrayscalars.h>

#include "fastnoisesimd/FastNoiseSIMD.h"

#define DEFAULT_SEED 42
#define CHARP(s) ((char *)(s))

/*
  The wrapper will map directly the C++ functions into Python functions.  
  Then we'll add a top-layer in Python to be more user friendly.

  We'll want to use PyArray_SimpleNewFromData(int nd, npy_intp* dims, int typenum, void* data)
  for making NumPy arrays.

  https://docs.scipy.org/doc/numpy/reference/c-api.array.html#creating-arrays

  There might be a small memory leak as we won't call the FastNoiseSIMD::Free
  
  Releasing GIL:
  Py_BEGIN_ALLOW_THREADS
  <...>
  Py_END_ALLOW_THREADS


 */

// Factory object
struct FNSObject
{
    PyObject_HEAD
    FastNoiseSIMD *fns;
};

static void
FNS_dealloc(FNSObject *self)
{
    // delete self->fns;
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *
FNS_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    FNSObject *self = (FNSObject *)type->tp_alloc(type, 0);

    if (self != NULL)
    {
        self->fns = NULL;
    }
    Py_INCREF(Py_None);
    return (PyObject *)self;
}

static int
FNS_init(FNSObject *self, PyObject *args, PyObject *kwargs)
{
    int seed = DEFAULT_SEED;

    static char *kwlist[] = {CHARP("seed"), NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|i", kwlist, &seed))
    {
        PyErr_Format(PyExc_RuntimeError,
                     "wrapper.cpp: Could not parse input arguments.");
        return -1;
    }

    self->fns = FastNoiseSIMD::NewFastNoiseSIMD(seed);

    Py_INCREF(Py_None);
    return 0;
}

// Note that in FastNoiseSIMD.h the arrays are called (x,y,z) but here we
// use the conventional (z,y,x) notation.  I.e. the z-axis is the slowest
// changing axis, and adjacent x-axis elements are adjacent in memory.

/*
PyDoc_STRVAR(GetEmptySet__doc__,
             "GetEmptySet(int size) -- Create an empty (aligned) noise set for use with FillNoiseSet().\n");
static PyObject *
PyFNS_GetEmptySet(PyObject *self, PyObject *args)
{
    // Make a NumPy array and return it. Note the array is empty, not zeroed.
    npy_intp dims[3] = {0, 0, 0};
    int ndim;
    const char *format = "n|nn";
    float *data;
    npy_intp size;
    PyObject *noiseArray;

    if (!PyArg_ParseTuple(args, format, &dims[0], &dims[1], &dims[2])) {
        return NULL;
    }

    // If any of the dims is zero, that dimension should not be present.
    // This can be the minor-most dimension `dims[2]` first and then `dims[1]`.
    // printf("Empty set got dims: %d, %d, %d\n", dims[0], dims[1], dims[2]);
    if (dims[1] == 0) {        // 1D
        ndim = 1;
        size = dims[0];
    } else if (dims[2] == 0) { // 2D 
        ndim = 2;
        size = dims[0] * dims[1];
    } else {                   // 3D
        ndim = 3;
        size = dims[0] * dims[1] * dims[2];
    }
    npy_intp aligned_size = FastNoiseSIMD::AlignedSize(size);
    printf("EmptySet for size: %d, aligned_size: %d\n", size, aligned_size);

    data = FastNoiseSIMD::GetEmptySet((int)size);
    printf("Alloc EmptySet @%p\n", data); fflush(NULL);
    noiseArray = PyArray_SimpleNewFromData(ndim, dims, NPY_FLOAT32, data);
    // As `AlignedArray` calls FreeNoiseSet we do _not_ set this array to 
    // own its data. In any case, the length of data can be longer than what 
    // NumPy thinks it is.
    // PyArray_ENABLEFLAGS((PyArrayObject *)noiseArray, NPY_ARRAY_OWNDATA);
    return noiseArray;
}
*/

/*
PyDoc_STRVAR(FreeNoiseSet__doc__,
             "FreeNoiseSet(AlignedArray noiseArray) -- Frees memory allocated with aligned_alloc or platform specific methods.\n");
static PyObject *
PyFNS_FreeNoiseSet(PyObject *self, PyObject *args)
{
    // Free the previously allocated aligned memory region.
    npy_intp dims[3] = {0, 0, 0};
    const char *format = "O";
    float *data;
    PyObject *noiseArray;

    if (!PyArg_ParseTuple(args, format, &noiseArray)) {
        return NULL;
    }

    data = (float *)PyArray_DATA((PyArrayObject *)noiseArray);
    printf("Free noise set @%p\n", data); fflush(NULL);
    FastNoiseSIMD::FreeNoiseSet(data);
    Py_RETURN_NONE;
}
*/

PyDoc_STRVAR(AlignedSize__doc__,
             "AlignedSize(int size) -- Rounds the size up to the nearest aligned size for the current SIMD level.\n");
static PyObject *
PyFNS_AlignedSize(PyObject *self, PyObject *args)
{
    int size;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &size))
    {
        return NULL;
    }
    return Py_BuildValue("i", FastNoiseSIMD::AlignedSize(size));
}

PyDoc_STRVAR(GetSeed__doc__,
             "int GetSeed() -- Returns seed used for all noise types.\n");
static PyObject *
PyFNS_GetSeed(FNSObject *self, PyObject *args)
{
    return Py_BuildValue("i", self->fns->GetSeed());
}

PyDoc_STRVAR(SetSeed__doc__,
             "SetSeed(int seed) -- Sets seed used for all noise types. Default is 42.\n");
static PyObject *
PyFNS_SetSeed(FNSObject *self, PyObject *args)
{
    int seed;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &seed))
    {
        return NULL;
    }
    self->fns->SetSeed(seed);
    Py_RETURN_NONE;
}

// Sets frequency for all noise types
PyDoc_STRVAR(SetFrequency__doc__,
             "SetFrequency(float frequency) -- Sets frequency for all noise types. Default: 0.01\n");
static PyObject *
PyFNS_SetFrequency(FNSObject *self, PyObject *args)
{
    float freq;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &freq))
    {
        return NULL;
    }
    self->fns->SetFrequency(freq);
    Py_RETURN_NONE;
}

// Sets noise return type of (Get/Fill)NoiseSet()
PyDoc_STRVAR(SetNoiseType__doc__,
             "SetNoiseType(NoiseType noiseType) --  Sets noise return type of (Get/Fill)NoiseSet(). Default: Simplex. Use the \
dict _ext.noiseType to convert names to enums.\n");
static PyObject *
PyFNS_SetNoiseType(FNSObject *self, PyObject *args)
{
    int type;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &type))
    {
        return NULL;
    }
    // TODO: check enum limits?
    self->fns->SetNoiseType((FastNoiseSIMD::NoiseType)type);
    Py_RETURN_NONE;
}

// Sets scaling factor for individual axis
PyDoc_STRVAR(SetAxesScales__doc__,
             "SetAxesScales(float zScale, float yScale, float xScale) --  Sets scaling factor for individual axis. Defaults: 1.0. \n");
static PyObject *
PyFNS_SetAxesScales(FNSObject *self, PyObject *args)
{
    float xScale, yScale, zScale;
    const char *format = "fff";

    if (!PyArg_ParseTuple(args, format, &zScale, &yScale, &xScale))
    {
        return NULL;
    }
    self->fns->SetAxesScales(zScale, yScale, xScale);
    Py_RETURN_NONE;
}

// Sets octave count for all fractal noise types
PyDoc_STRVAR(SetFractalOctaves__doc__,
             "SetFractalOctaves(int octaves) --  Sets octave count for all fractal noise types. Default: 3. \n");
static PyObject *
PyFNS_SetFractalOctaves(FNSObject *self, PyObject *args)
{
    int num;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &num))
    {
        return NULL;
    }
    // TODO: check octave limits?
    self->fns->SetFractalOctaves(num);
    Py_RETURN_NONE;
}

// Sets octave lacunarity for all fractal noise types
PyDoc_STRVAR(SetFractalLacunarity__doc__,
             "SetFractalLacunarity(float lacunarity) --  Sets octave lacunarity for all fractal noise types. Default: 2.0. \n");
static PyObject *
PyFNS_SetFractalLacunarity(FNSObject *self, PyObject *args)
{
    float lac;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &lac))
    {
        return NULL;
    }
    self->fns->SetFractalLacunarity(lac);
    Py_RETURN_NONE;
}

// Sets octave gain for all fractal noise types
// Default: 0.5
// void SetFractalGain(float gain) { m_gain = gain; m_fractalBounding = CalculateFractalBounding(m_octaves, m_gain); }
PyDoc_STRVAR(SetFractalGain__doc__,
             "SetFractalGain(float gain) --  Sets octave gain for all fractal noise types. Default: 0.5. \n");
static PyObject *
PyFNS_SetFractalGain(FNSObject *self, PyObject *args)
{
    float gain;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &gain))
    {
        return NULL;
    }
    self->fns->SetFractalGain(gain);
    Py_RETURN_NONE;
}

// Sets method for combining octaves in all fractal noise types
PyDoc_STRVAR(SetFractalType__doc__,
             "SetFractalType(int fractalType) --  Sets method for combining octaves in all fractal noise types. Default: FBM. \
Use the dict _ext.fractalType to convert names to enums.\n");
static PyObject *
PyFNS_SetFractalType(FNSObject *self, PyObject *args)
{
    int type;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &type))
    {
        return NULL;
    }
    // TODO: check enum limits?
    self->fns->SetFractalType((FastNoiseSIMD::FractalType)type);
    Py_RETURN_NONE;
}

// Sets return type from cellular noise calculations
PyDoc_STRVAR(SetCellularReturnType__doc__,
             "SetCellularReturnType(int cellularReturnType) --   Sets return type from cellular noise calculations. Default: \
Distance. Use the dict _ext.cellularReturnType to convert names to enums.\n");
static PyObject *
PyFNS_SetCellularReturnType(FNSObject *self, PyObject *args)
{
    int type;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &type))
    {
        return NULL;
    }
    // TODO: check enum limits?
    self->fns->SetCellularReturnType((FastNoiseSIMD::CellularReturnType)type);
    Py_RETURN_NONE;
}

// Sets distance function used in cellular noise calculations
PyDoc_STRVAR(SetCellularDistanceFunction__doc__,
             "SetCellularDistanceFunction(int cellularDistanceFunction) --   Sets distance function used in cellular noise \
calculations. Default: Euclidean. Use the dict _ext.cellularDistanceFunction to convert names to enums.\n");
static PyObject *
PyFNS_SetCellularDistanceFunction(FNSObject *self, PyObject *args)
{
    int type;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &type))
    {
        return NULL;
    }
    // TODO: check enum limits?
    self->fns->SetCellularDistanceFunction((FastNoiseSIMD::CellularDistanceFunction)type);
    Py_RETURN_NONE;
}

// Sets the type of noise used if cellular return type is set to NoiseLookup
PyDoc_STRVAR(SetCellularNoiseLookupType__doc__,
             "SetCellularNoiseLookupType(int cellularNoiseLookupType)--  Sets the type of noise used if cellular return type is \
set to NoiseLookup. Default: Simplex. Use the dict _ext.noiseType to convert names to enums.\n");
static PyObject *
PyFNS_SetCellularNoiseLookupType(FNSObject *self, PyObject *args)
{
    int type;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &type))
    {
        return NULL;
    }
    // TODO: check enum limits?
    self->fns->SetCellularNoiseLookupType((FastNoiseSIMD::NoiseType)type);
    Py_RETURN_NONE;
}

// Sets relative frequency on the cellular noise lookup return type
PyDoc_STRVAR(SetCellularNoiseLookupFrequency__doc__,
             "SetCellularNoiseLookupFrequency(float cellularNoiseLookupFrequency) -- Sets relative frequency on the cellular noise \
lookup return type. Default: 0.2\n");
static PyObject *
PyFNS_SetCellularNoiseLookupFrequency(FNSObject *self, PyObject *args)
{
    float freq;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &freq))
    {
        return NULL;
    }
    self->fns->SetCellularNoiseLookupFrequency(freq);
    Py_RETURN_NONE;
}

// Sets the 2 distance indicies used for distance2 return types
PyDoc_STRVAR(SetCellularDistance2Indices__doc__,
             "SetCellularDistance2Indices(int cellularDistanceIndex0, int cellularDistanceIndex1) -- Sets the 2 distance indicies \
used for distance2 return types. Default: 0, 1. Note: index0 should be lower than index1, index1 must be < 4.\n");
static PyObject *
PyFNS_SetCellularDistance2Indices(FNSObject *self, PyObject *args)
{
    int index1, index2;
    const char *format = "ii";

    if (!PyArg_ParseTuple(args, format, &index1, &index2))
    {
        return NULL;
    }
    self->fns->SetCellularDistance2Indicies(index1, index2);
    Py_RETURN_NONE;
}

// Sets the maximum distance a cellular point can move from it's grid position
// Setting this high will make artifacts more common
// Default: 0.45
// void SetCellularJitter(float cellularJitter) { m_cellularJitter = cellularJitter; }
PyDoc_STRVAR(SetCellularJitter__doc__,
             "SetCellularJitter(float cellularJitter) -- Sets relative frequency on the cellular noise \
lookup return type. Default: 0.2\n");
static PyObject *
PyFNS_SetCellularJitter(FNSObject *self, PyObject *args)
{
    float jitter;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &jitter))
    {
        return NULL;
    }
    self->fns->SetCellularJitter(jitter);
    Py_RETURN_NONE;
}

// Enables position perturbing for all noise types
PyDoc_STRVAR(SetPerturbType__doc__,
             "SetPerturbType(int perturbType) --  Enables position perturbing for all noise types. Default: None. \
Use the dict _ext.perturbType to convert names to enums.\n");
static PyObject *
PyFNS_SetPerturbType(FNSObject *self, PyObject *args)
{
    int type;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &type))
    {
        return NULL;
    }
    // TODO: check enum limits?
    self->fns->SetPerturbType((FastNoiseSIMD::PerturbType)type);
    Py_RETURN_NONE;
}

// Sets the maximum distance the input position can be perturbed
PyDoc_STRVAR(SetPerturbAmp__doc__,
             "SetPerturbAmp(float perturbAmp) -- Sets the maximum distance the input position can be perturbed. Default: 1.0.\n");
static PyObject *
PyFNS_SetPerturbAmp(FNSObject *self, PyObject *args)
{
    float num;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &num))
    {
        return NULL;
    }
    self->fns->SetPerturbAmp(num);
    Py_RETURN_NONE;
}

// Set the relative frequency for the perturb gradient
PyDoc_STRVAR(SetPerturbFrequency__doc__,
             "SetPerturbFrequency(float perturbFrequency) -- Set the relative frequency for the perturb gradient. Default: 0.5.\n");
static PyObject *
PyFNS_SetPerturbFrequency(FNSObject *self, PyObject *args)
{
    float num;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &num))
    {
        return NULL;
    }
    self->fns->SetPerturbFrequency(num);
    Py_RETURN_NONE;
}

// Sets octave count for perturb fractal types
PyDoc_STRVAR(SetPerturbFractalOctaves__doc__,
             "SetPerturbFractalOctaves(int perturbOctaves)--  Sets octave count for perturb fractal types. Default: 3.\n");
static PyObject *
PyFNS_SetPerturbFractalOctaves(FNSObject *self, PyObject *args)
{
    int num;
    const char *format = "i";

    if (!PyArg_ParseTuple(args, format, &num))
    {
        return NULL;
    }
    // TODO: check enum limits?
    self->fns->SetPerturbFractalOctaves(num);
    Py_RETURN_NONE;
}

// Sets octave lacunarity for perturb fractal types
PyDoc_STRVAR(SetPerturbFractalLacunarity__doc__,
             "SetPerturbFractalLacunarity(float perturbLacunarity) -- Sets octave lacunarity for perturb fractal types. Default: 2.0.\n");
static PyObject *
PyFNS_SetPerturbFractalLacunarity(FNSObject *self, PyObject *args)
{
    float num;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &num))
    {
        return NULL;
    }
    self->fns->SetPerturbFractalLacunarity(num);
    Py_RETURN_NONE;
}

// Sets octave gain for perturb fractal types
PyDoc_STRVAR(SetPerturbFractalGain__doc__,
             "SetPerturbFractalGain(float perturbGain) -- Sets octave gain for perturb fractal types. Default: 0.5.\n");
static PyObject *
PyFNS_SetPerturbFractalGain(FNSObject *self, PyObject *args)
{
    float num;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &num))
    {
        return NULL;
    }
    self->fns->SetPerturbFractalGain(num);
    Py_RETURN_NONE;
}

// Sets the length for vectors after perturb normalising
PyDoc_STRVAR(SetPerturbNormaliseLength__doc__,
             "SetPerturbNormaliseLength(float perturbGain) -- Sets the length for vectors after perturb normalising . Default: 1.0.\n");
static PyObject *
PyFNS_SetPerturbNormaliseLength(FNSObject *self, PyObject *args)
{
    float num;
    const char *format = "f";

    if (!PyArg_ParseTuple(args, format, &num))
    {
        return NULL;
    }
    self->fns->SetPerturbNormaliseLength(num);
    Py_RETURN_NONE;
}

// For now just implement the 'get' functions
// The vector set we would have to create a custom object for
// static FastNoiseVectorSet* GetVectorSet(int xSize, int ySize, int zSize);

/*
// float* GetNoiseSet(int xStart, int yStart, int zStart, int xSize, int ySize, int zSize, float scaleModifier = 1.0f);
PyDoc_STRVAR(GetNoiseSet__doc__,
             "GetNoiseSet(int xStart, int yStart, int zStart, int xSize, int ySize, int zSize, float scaleModifier = 1.0f)\
-- Create a noise set.\n");
static PyObject *
PyFNS_GetNoiseSet(FNSObject *self, PyObject *args)
{
    // Make a NumPy array and return it. Note the array is empty, not zeroed.
    int xStart, yStart, zStart;
    npy_intp dims[3] = {0, 0, 0};
    float scaleMod = 1.0;
    const char *format = "iiinnn|f";
    float *data = NULL;
    PyObject *noiseArray;

    if (!PyArg_ParseTuple(args, format, &zStart, &yStart, &xStart, &dims[0], &dims[1], &dims[2], &scaleMod))
    {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS // Release GIL
    data = self->fns->GetNoiseSet(zStart, yStart, xStart, (int)dims[0], (int)dims[1], (int)dims[2], scaleMod);
    Py_END_ALLOW_THREADS

    noiseArray = PyArray_SimpleNewFromData(3, dims, NPY_FLOAT32, data);
    PyArray_ENABLEFLAGS((PyArrayObject *)noiseArray, NPY_ARRAY_OWNDATA);
    return noiseArray;
}
*/

// void FastNoiseSIMD::FillNoiseSet(float* noiseSet, int xStart, int yStart, int zStart, int xSize, int ySize, int zSize, float scaleModifier)
PyDoc_STRVAR(FillNoiseSet__doc__,
    "FillNoiseSet(float* noiseSet, int xStart, int yStart, int zStart, int xSize, int ySize, int zSize, float scaleModifier)\
-- Fill a noise set.\n");
static PyObject *
PyFNS_FillNoiseSet(FNSObject *self, PyObject *args)
{
    // Fill an existing empty array, used for multi-threaded operation
    PyObject* noiseObj;
    float* noisePtr;
    int xStart, yStart, zStart;
    int dims[3] = {0, 0, 0};
    float scaleMod = 1.0;
    const char *format = "Oiiiiii|f";

    if (!PyArg_ParseTuple(args, format, &noiseObj, &zStart, &yStart, &xStart, &dims[0], &dims[1], &dims[2], &scaleMod))
    {
        return NULL;
    }

    noisePtr = (float *)PyArray_DATA((PyArrayObject *)noiseObj);

    Py_BEGIN_ALLOW_THREADS // Release GIL
    self->fns->FillNoiseSet(noisePtr, zStart, yStart, xStart, dims[0], dims[1], dims[2], scaleMod);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

/*
PyDoc_STRVAR(NoiseFromCoords__doc__,
    "NoiseFromCoords(numpy.ndarray noise, numpy.ndarray coords)\
-- Fill a noise set from arbitrary coordinates. Must be a shape (3,N) array of dtype 'float32'. \n");
static PyObject *
PyFNS_NoiseFromCoords(FNSObject *self, PyObject *args)
{
    PyObject *noiseObj;
    PyObject *coordsObj;
    FastNoiseVectorSet vector;
    npy_intp size, offset;
    float *noisePtr;
    const char *format = "OOnn";
    // We pass in `size` so we can chunk arrays for multi-threaded operations.
    if (!PyArg_ParseTuple(args, format, &noiseObj, &coordsObj, &size, &offset)) 
    {
        return NULL;
    }
    noisePtr = (float *)PyArray_GETPTR1((PyArrayObject *)noiseObj, offset);

    // Typical confusion here, Numpy is [Z,Y,X], whereas PyFastNoiseSIMD is [X,Y,Z]
    // but it makes no difference in the result, as long as we obey C-ordering
    vector.xSet = (float *)PyArray_GETPTR2((PyArrayObject *)coordsObj, 0, offset);
    vector.ySet = (float *)PyArray_GETPTR2((PyArrayObject *)coordsObj, 1, offset);
    vector.zSet = (float *)PyArray_GETPTR2((PyArrayObject *)coordsObj, 2, offset);
    vector.size = (int)size;

    Py_BEGIN_ALLOW_THREADS // Release GIL
    self->fns->FillNoiseSet(noisePtr, &vector, 0.0f, 0.0f, 0.0f);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}
*/

PyDoc_STRVAR(NoiseFromCoords__doc__,
    "NoiseFromCoords(numpy.ndarray noise, numpy.ndarray coords)\
-- Fill a noise set from arbitrary coordinates. Must be a shape (3,N) array of dtype 'float32'. \n");
static PyObject *
PyFNS_NoiseFromCoords(FNSObject *self, PyObject *args)
{
    PyObject *noiseObj;
    PyObject *xObj, *yObj, *zObj;
    FastNoiseVectorSet vector;
    npy_intp size, offset;
    float *noisePtr;
    const char *format = "OOOOnn";
    // We pass in `size` so we can chunk arrays for multi-threaded operations.
    if (!PyArg_ParseTuple(args, format, &noiseObj, &xObj, &yObj, &zObj, &size, &offset)) 
    {
        return NULL;
    }
    noisePtr = (float *)PyArray_GETPTR1((PyArrayObject *)noiseObj, offset);

    // Typical confusion here, Numpy is [Z,Y,X], whereas PyFastNoiseSIMD is [X,Y,Z]
    // but it makes no difference in the result, as long as we obey C-ordering
    vector.xSet = (float *)PyArray_GETPTR1((PyArrayObject *)xObj, offset);
    vector.ySet = (float *)PyArray_GETPTR1((PyArrayObject *)yObj, offset);
    vector.zSet = (float *)PyArray_GETPTR1((PyArrayObject *)zObj, offset);
    vector.size = (int)size;

    // printf("EXT: Vector alignment error: (%lld, %lld, %lld)\n", 
    //     (npy_intp)vector.xSet % 8, (npy_intp)vector.ySet % 8, (npy_intp)vector.zSet % 8);

    Py_BEGIN_ALLOW_THREADS // Release GIL
    self->fns->FillNoiseSet(noisePtr, &vector, 0.0f, 0.0f, 0.0f);
    Py_END_ALLOW_THREADS

    Py_RETURN_NONE;
}

/*
Work in Progress: Map projections, starting with Kavraisky 7

#define PI 3.141592653589793
PyDoc_STRVAR(ProjectKav7__doc__,
    "ProjectKav7(float radius, float tile_size, float p0, float l0)\
-- Make a Kavraiskiy 7 projection from noise mapped to a sphere. \n");
static PyObject *
PyFNS_ProjectKav7(FNSObject *self, PyObject *args) {
    // UNFINISHED
    npy_float32 radius, alpha;
    npy_float32 tile_size = 40.0f;
    npy_float32 p0 = 0.0f;
    npy_float32 l0 = 0.0f;
    npy_intp x_max, y_max;
    npy_float64 phi;
    const char *format = "f|fff";

    if (!PyArg_ParseTuple(args, format, &radius, &tile_size, &p0, &l0)) {
        return NULL;
    }

    alpha = radius / tile_size;
    // Dimensions/mask
    // Then how many steps in x as a function of distance from equator?
    // y_max = 0.5*pi*alpha = 1.5707963267948966 * alpha
    y_max = (npy_intp)(1.5707963267948966 * alpha);
    // x_max = 1.5*sqrt(1/3)*pi*alpha = 2.7206990463513265 * alpha
    x_max= (npy_intp)(2.7206990463513265 * alpha);
    // Total map shape is [2*y_shape, 2*x_shape]

    // Generate empty coords

    // Allocate a 2D array for the greyscale noise result


    // TODO: drop the GIL


    // TODO: re-acquire the GIL


    phi = -PI/2.0;

    // TODO: return a numpy array.
    Py_RETURN_NONE;
}
*/

static PyMethodDef FNS_methods[] = {
    {"GetSeed", (PyCFunction)PyFNS_GetSeed, METH_VARARGS, GetSeed__doc__},
    {"SetSeed", (PyCFunction)PyFNS_SetSeed, METH_VARARGS, SetSeed__doc__},
    {"SetFrequency", (PyCFunction)PyFNS_SetFrequency, METH_VARARGS, SetFrequency__doc__},
    {"SetNoiseType", (PyCFunction)PyFNS_SetNoiseType, METH_VARARGS, SetNoiseType__doc__},
    {"SetAxesScales", (PyCFunction)PyFNS_SetAxesScales, METH_VARARGS, SetAxesScales__doc__},
    {"SetFractalOctaves", (PyCFunction)PyFNS_SetFractalOctaves, METH_VARARGS, SetFractalOctaves__doc__},
    {"SetFractalLacunarity", (PyCFunction)PyFNS_SetFractalLacunarity, METH_VARARGS, SetFractalLacunarity__doc__},
    {"SetFractalGain", (PyCFunction)PyFNS_SetFractalGain, METH_VARARGS, SetFractalGain__doc__},
    {"SetFractalType", (PyCFunction)PyFNS_SetFractalType, METH_VARARGS, SetFractalType__doc__},
    {"SetCellularReturnType", (PyCFunction)PyFNS_SetCellularReturnType, METH_VARARGS, SetCellularReturnType__doc__},
    {"SetCellularDistanceFunction", (PyCFunction)PyFNS_SetCellularDistanceFunction, METH_VARARGS, SetCellularDistanceFunction__doc__},
    {"SetCellularNoiseLookupType", (PyCFunction)PyFNS_SetCellularNoiseLookupType, METH_VARARGS, SetCellularNoiseLookupType__doc__},
    {"SetCellularNoiseLookupFrequency", (PyCFunction)PyFNS_SetCellularNoiseLookupFrequency, METH_VARARGS, SetCellularNoiseLookupFrequency__doc__},
    {"SetCellularDistance2Indices", (PyCFunction)PyFNS_SetCellularDistance2Indices, METH_VARARGS, SetCellularDistance2Indices__doc__},
    {"SetCellularJitter", (PyCFunction)PyFNS_SetCellularJitter, METH_VARARGS, SetCellularJitter__doc__},
    {"SetPerturbType", (PyCFunction)PyFNS_SetPerturbType, METH_VARARGS, SetPerturbType__doc__},
    {"SetPerturbAmp", (PyCFunction)PyFNS_SetPerturbAmp, METH_VARARGS, SetPerturbAmp__doc__},
    {"SetPerturbFrequency", (PyCFunction)PyFNS_SetPerturbFrequency, METH_VARARGS, SetPerturbFrequency__doc__},
    {"SetPerturbFractalOctaves", (PyCFunction)PyFNS_SetPerturbFractalOctaves, METH_VARARGS, SetPerturbFractalOctaves__doc__},
    {"SetPerturbFractalLacunarity", (PyCFunction)PyFNS_SetPerturbFractalLacunarity, METH_VARARGS, SetPerturbFractalLacunarity__doc__},
    {"SetPerturbFractalGain", (PyCFunction)PyFNS_SetPerturbFractalGain, METH_VARARGS, SetPerturbFractalGain__doc__},
    {"SetPerturbNormaliseLength", (PyCFunction)PyFNS_SetPerturbNormaliseLength, METH_VARARGS, SetPerturbNormaliseLength__doc__},
    // {"GetNoiseSet", (PyCFunction)PyFNS_GetNoiseSet, METH_VARARGS, GetNoiseSet__doc__},
    {"FillNoiseSet", (PyCFunction)PyFNS_FillNoiseSet, METH_VARARGS, FillNoiseSet__doc__},
    {"NoiseFromCoords", (PyCFunction)PyFNS_NoiseFromCoords, METH_VARARGS, NoiseFromCoords__doc__},
    // {"ProjectKav7", (PyCFunction)PyFNS_ProjectKav7, METH_VARARGS, ProjectKav7__doc__},
    {NULL, NULL, 0, NULL},
};


PyTypeObject FNSType = {
    PyVarObject_HEAD_INIT(NULL, 0) "pyfastnoisesimd.extension.FNS", /*tp_name*/
    sizeof(FNSObject),                                              /*tp_basicsize*/
    0,                                                              /*tp_itemsize*/
    (destructor)FNS_dealloc,                                        /*tp_dealloc*/
    0,                                                              /*tp_print*/
    0,                                                              /*tp_getattr*/
    0,                                                              /*tp_setattr*/
    0,                                                              /*tp_compare*/
    0,                                                              /*tp_repr*/
    0,                                                              /*tp_as_number*/
    0,                                                              /*tp_as_sequence*/
    0,                                                              /*tp_as_mapping*/
    0,                                                              /*tp_hash */
    0,                                                              /*tp_call*/
    0,                                                              /*tp_str*/
    0,                                                              /*tp_getattro*/
    0,                                                              /*tp_setattro*/
    0,                                                              /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                       /*tp_flags*/
    "FastNoiseSIMD factory",                                        /* tp_doc */
    0,                                                              /* tp_traverse */
    0,                                                              /* tp_clear */
    0,                                                              /* tp_richcompare */
    0,                                                              /* tp_weaklistoffset */
    0,                                                              /* tp_iter */
    0,                                                              /* tp_iternext */
    FNS_methods,                                                    /* tp_methods */
    0,                                                              /* tp_members */
    0,                                                              /* tp_getset */
    0,                                                              /* tp_base */
    0,                                                              /* tp_dict */
    0,                                                              /* tp_descr_get */
    0,                                                              /* tp_descr_set */
    0,                                                              /* tp_dictoffset */
    (initproc)FNS_init,                                             /* tp_init */
    0,                                                              /* tp_alloc */
    FNS_new,                                                        /* tp_new */
};

static PyMethodDef module_methods[] =
    {
        //{"EmptySet", (PyCFunction)PyFNS_GetEmptySet, METH_VARARGS, GetEmptySet__doc__},
        //{"GetSIMDAlignment", (PyCFunction)PyFNS_GetSIMDAlignment, METH_VARARGS, GetSIMDAlignment__doc__},
        //{"FreeSet", (PyCFunction)PyFNS_FreeNoiseSet, METH_VARARGS, FreeNoiseSet__doc__},
        {"AlignedSize", (PyCFunction)PyFNS_AlignedSize, METH_VARARGS, AlignedSize__doc__},
        {NULL, NULL},
};

// Python 3 module initialization
static struct PyModuleDef module_def = {
    PyModuleDef_HEAD_INIT,
    "extension",
    NULL,
    -1,
    module_methods,
    NULL,
    NULL,
    NULL,
    NULL};

PyMODINIT_FUNC
PyInit_extension(void)
{
    PyObject *dictNoiseType, *dictFractalType, *dictPerturbType;
    PyObject *dictCellularDistanceFunction, *dictCellularReturnType;
    
    // WARNING: PyType_Ready MUST be called to finalize new Python types before
    // a module is created. Official documentation is weak on this point.
    if (PyType_Ready(&FNSType) < 0)
    {
        PyErr_Format(PyExc_RuntimeError, "FNSType not ready.\n");
        return NULL;
    }

    PyObject *m = PyModule_Create(&module_def);
    if (m == NULL)
    {
        PyErr_Format(PyExc_RuntimeError, "Python interpreter not started.\n");
        return NULL;
    }

    Py_INCREF(&FNSType);
    PyModule_AddObject(m, "FNS", (PyObject *)&FNSType);

    import_array(); // Import Numpy

    // Dictionary enum maps
    // enum NoiseType { Value, ValueFractal, Perlin, PerlinFractal, Simplex,
    //   SimplexFractal, WhiteNoise, Cellular, Cubic, CubicFractal };
    dictNoiseType = PyDict_New();
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "Value"), Py_BuildValue("i", FastNoiseSIMD::Value));
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "ValueFractal"), Py_BuildValue("i", FastNoiseSIMD::ValueFractal));
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "Perlin"), Py_BuildValue("i", FastNoiseSIMD::Perlin));
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "PerlinFractal"), Py_BuildValue("i", FastNoiseSIMD::PerlinFractal));
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "Simplex"), Py_BuildValue("i", FastNoiseSIMD::Simplex));
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "SimplexFractal"), Py_BuildValue("i", FastNoiseSIMD::SimplexFractal));
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "WhiteNoise"), Py_BuildValue("i", FastNoiseSIMD::WhiteNoise));
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "Cellular"), Py_BuildValue("i", FastNoiseSIMD::Cellular));
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "Cubic"), Py_BuildValue("i", FastNoiseSIMD::Cubic));
    PyDict_SetItem(dictNoiseType, Py_BuildValue("s", "CubicFractal"), Py_BuildValue("i", FastNoiseSIMD::CubicFractal));
    PyModule_AddObject(m, "noiseType", dictNoiseType);

    // enum FractalType { FBM, Billow, RigidMulti };
    dictFractalType = PyDict_New();
    PyDict_SetItem(dictFractalType, Py_BuildValue("s", "FBM"), Py_BuildValue("i", FastNoiseSIMD::FBM));
    PyDict_SetItem(dictFractalType, Py_BuildValue("s", "Billow"), Py_BuildValue("i", FastNoiseSIMD::Billow));
    PyDict_SetItem(dictFractalType, Py_BuildValue("s", "RigidMulti"), Py_BuildValue("i", FastNoiseSIMD::RigidMulti));
    PyModule_AddObject(m, "fractalType", dictFractalType);

    // enum PerturbType { None, Gradient, GradientFractal, Normalise,
    //   Gradient_Normalise, GradientFractal_Normalise };
    dictPerturbType = PyDict_New();
    PyDict_SetItem(dictPerturbType, Py_None, Py_BuildValue("i", FastNoiseSIMD::None));
    PyDict_SetItem(dictPerturbType, Py_BuildValue("s", "Gradient"), Py_BuildValue("i", FastNoiseSIMD::Gradient));
    PyDict_SetItem(dictPerturbType, Py_BuildValue("s", "GradientFractal"), Py_BuildValue("i", FastNoiseSIMD::GradientFractal));
    PyDict_SetItem(dictPerturbType, Py_BuildValue("s", "Normalise"), Py_BuildValue("i", FastNoiseSIMD::Normalise));
    PyDict_SetItem(dictPerturbType, Py_BuildValue("s", "Gradient_Normalise"), Py_BuildValue("i", FastNoiseSIMD::Gradient_Normalise));
    PyDict_SetItem(dictPerturbType, Py_BuildValue("s", "GradientFractal_Normalise"), Py_BuildValue("i", FastNoiseSIMD::GradientFractal_Normalise));
    PyModule_AddObject(m, "perturbType", dictPerturbType);

    // enum CellularDistanceFunction { Euclidean, Manhattan, Natural };
    dictCellularDistanceFunction = PyDict_New();
    PyDict_SetItem(dictCellularDistanceFunction, Py_BuildValue("s", "Euclidean"), Py_BuildValue("i", FastNoiseSIMD::Euclidean));
    PyDict_SetItem(dictCellularDistanceFunction, Py_BuildValue("s", "Manhattan"), Py_BuildValue("i", FastNoiseSIMD::Manhattan));
    PyDict_SetItem(dictCellularDistanceFunction, Py_BuildValue("s", "Natural"), Py_BuildValue("i", FastNoiseSIMD::Natural));
    PyModule_AddObject(m, "cellularDistanceFunction", dictCellularDistanceFunction);

    // enum CellularReturnType { CellValue, Distance, Distance2, Distance2Add,
    //   Distance2Sub, Distance2Mul, Distance2Div, NoiseLookup, Distance2Cave };
    dictCellularReturnType = PyDict_New();
    PyDict_SetItem(dictCellularReturnType, Py_BuildValue("s", "CellValue"), Py_BuildValue("i", FastNoiseSIMD::CellValue));
    PyDict_SetItem(dictCellularReturnType, Py_BuildValue("s", "Distance"), Py_BuildValue("i", FastNoiseSIMD::Distance));
    PyDict_SetItem(dictCellularReturnType, Py_BuildValue("s", "Distance2"), Py_BuildValue("i", FastNoiseSIMD::Distance2));
    PyDict_SetItem(dictCellularReturnType, Py_BuildValue("s", "Distance2Add"), Py_BuildValue("i", FastNoiseSIMD::Distance2Add));
    PyDict_SetItem(dictCellularReturnType, Py_BuildValue("s", "Distance2Sub"), Py_BuildValue("i", FastNoiseSIMD::Distance2Sub));
    PyDict_SetItem(dictCellularReturnType, Py_BuildValue("s", "Distance2Mul"), Py_BuildValue("i", FastNoiseSIMD::Distance2Mul));
    PyDict_SetItem(dictCellularReturnType, Py_BuildValue("s", "Distance2Div"), Py_BuildValue("i", FastNoiseSIMD::Distance2Div));
    PyDict_SetItem(dictCellularReturnType, Py_BuildValue("s", "NoiseLookup"), Py_BuildValue("i", FastNoiseSIMD::NoiseLookup));
    PyDict_SetItem(dictCellularReturnType, Py_BuildValue("s", "Distance2Cave"), Py_BuildValue("i", FastNoiseSIMD::Distance2Cave));
    PyModule_AddObject(m, "cellularReturnType", dictCellularReturnType);

    // Load SIMD level into module
    FastNoiseSIMD *dummy = FastNoiseSIMD::NewFastNoiseSIMD(1);
    int simd_level = dummy->GetSIMDLevel();
    delete dummy;
    switch(simd_level) {
        case FN_SSE2:
            PyModule_AddIntConstant(m, "SIMD_ALIGNMENT", 16);
            PyModule_AddStringConstant(m, "SIMD_LEVEL", "SSE2");
            break;
        case FN_SSE41:
            PyModule_AddIntConstant(m, "SIMD_ALIGNMENT", 16);
            PyModule_AddStringConstant(m, "SIMD_LEVEL", "SSE4.1");
            break;
        case FN_AVX2:
            PyModule_AddIntConstant(m, "SIMD_ALIGNMENT", 32);
            PyModule_AddStringConstant(m, "SIMD_LEVEL", "AVX2");
            break;
        case FN_AVX512:
            PyModule_AddIntConstant(m, "SIMD_ALIGNMENT", 64);
            PyModule_AddStringConstant(m, "SIMD_LEVEL", "AVX512");
            break;
        case FN_NEON:
            PyModule_AddIntConstant(m, "SIMD_ALIGNMENT", 16);
            PyModule_AddStringConstant(m, "SIMD_LEVEL", "ARM NEON");
            break;
        default: // FN_NO_SIMD_FALLBACK
            PyModule_AddIntConstant(m, "SIMD_ALIGNMENT", 2);
            PyModule_AddStringConstant(m, "SIMD_LEVEL", "Fallback");
    }

    return m;
}

#endif // FASTNOISE_SIMD_WRAPPER_CPP
