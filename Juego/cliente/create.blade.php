@extends('layouts.admin')
@section('contenido')
  <div class="row">
    <div class="col-lg-6 col-md-6 col-sm-6 col-xs-6">
      <h3>Nueva articulo</h3>
      <label>En mantenimiento</label>
      @if (count($errors)>0)
      <div class="alert alert-danger">
        <ul>
          @foreach ($errors -> all() as $error)
            <li>{{$error}}</li>
          @endforeach
        </ul>
      </div>
    @endif
  </div>
</div>
@endsection
