;(function(){ 'use strict';

  // registers the extension on a cytoscape lib ref
  var register = function( cytoscape, $ ){
    if( !cytoscape ){ return; } // can't register if cytoscape unspecified

    $.fn.cyPanzoom = $.fn.cytoscapePanzoom = function( options ){
      panzoom.apply( this, [ options ] );

      return this; // chainability
    };

    // if you want a core extension
    cytoscape('core', 'panzoom', function( options ){ // could use options object, but args are up to you
      var cy = this;

      panzoom.apply( cy.container(), [ options ] );

      return this; // chainability
    });

  };

  var defaults = {
    zoomFactor: 0.05, // zoom factor per zoom tick
    zoomDelay: 45, // how many ms between zoom ticks
    minZoom: 0.1, // min zoom level
    maxZoom: 10, // max zoom level
    fitPadding: 50, // padding when fitting
    panSpeed: 10, // how many ms in between pan ticks
    panDistance: 10, // max pan distance per tick
    panDragAreaSize: 75, // the length of the pan drag box in which the vector for panning is calculated (bigger = finer control of pan speed and direction)
    panMinPercentSpeed: 0.25, // the slowest speed we can pan by (as a percent of panSpeed)
    panInactiveArea: 8, // radius of inactive area in pan drag box
    panIndicatorMinOpacity: 0.5, // min opacity of pan indicator (the draggable nib); scales from this to 1.0
    zoomOnly: false, // a minimal version of the ui only with zooming (useful on systems with bad mousewheel resolution)

    // icon class names
    sliderHandleIcon: 'fa fa-minus',
    zoomInIcon: 'fa fa-plus',
    zoomOutIcon: 'fa fa-minus',
    resetIcon: 'fa fa-expand'
  };

  var panzoom = function(params){
    var options = $.extend(true, {}, defaults, params);
    var fn = params;

    var functions = {
      destroy: function(){
        var $this = $(this);
        var $pz = $this.find(".cy-panzoom");

        $pz.data('winbdgs').forEach(function( l ){
          $(window).unbind( l.evt, l.fn );
        });

        $pz.data('cybdgs').forEach(function( l ){
          $(this).cytoscape('get').off( l.evt, l.fn );
        });

        $pz.remove();
      },

      init: function(){
        var browserIsMobile = 'ontouchstart' in window;

        return $(this).each(function(){
          var $container = $(this);

          var winbdgs = [];
          var $win = $(window);

          var windowBind = function( evt, fn ){
            winbdgs.push({ evt: evt, fn: fn });

            $win.bind( evt, fn );
          };

          var windowUnbind = function( evt, fn ){
            for( var i = 0; i < winbdgs.length; i++ ){
              var l = winbdgs[i];

              if( l.evt === evt && l.fn === fn ){
                winbdgs.splice( i, 1 );
                break;
              }
            }

            $win.unbind( evt, fn );
          };

          var cybdgs = [];
          var cy = $container.cytoscape('get');

          var cyOn = function( evt, fn ){
            cybdgs.push({ evt: evt, fn: fn });

            cy.on( evt, fn );
          };

          var cyOff = function( evt, fn ){
            for( var i = 0; i < cybdgs.length; i++ ){
              var l = cybdgs[i];

              if( l.evt === evt && l.fn === fn ){
                cybdgs.splice( i, 1 );
                break;
              }
            }

            cy.off( evt, fn );
          };

          var $panzoom = $('<div class="cy-panzoom"></div>');
          $container.append( $panzoom );

          $panzoom.data('winbdgs', winbdgs);
          $panzoom.data('cybdgs', cybdgs);

          if( options.zoomOnly ){
            $panzoom.addClass("cy-panzoom-zoom-only");
          }

          // add base html elements
          /////////////////////////

          var $zoomIn = $('<div class="cy-panzoom-zoom-in cy-panzoom-zoom-button"><span class="icon '+ options.zoomInIcon +'"></span></div>');
          $panzoom.append( $zoomIn );

          var $zoomOut = $('<div class="cy-panzoom-zoom-out cy-panzoom-zoom-button"><span class="icon ' + options.zoomOutIcon + '"></span></div>');
          $panzoom.append( $zoomOut );

          var $reset = $('<div class="cy-panzoom-reset cy-panzoom-zoom-button"><span class="icon ' + options.resetIcon + '"></span></div>');
          $panzoom.append( $reset );

          var $slider = $('<div class="cy-panzoom-slider"></div>');
          $panzoom.append( $slider );

          $slider.append('<div class="cy-panzoom-slider-background"></div>');

          var $sliderHandle = $('<div class="cy-panzoom-slider-handle"><span class="icon ' + options.sliderHandleIcon + '"></span></div>');
          $slider.append( $sliderHandle );

          var $noZoomTick = $('<div class="cy-panzoom-no-zoom-tick"></div>');
          $slider.append( $noZoomTick );

          var $panner = $('<div class="cy-panzoom-panner"></div>');
          $panzoom.append( $panner );

          var $pHandle = $('<div class="cy-panzoom-panner-handle"></div>');
          $panner.append( $pHandle );

          var $pUp = $('<div class="cy-panzoom-pan-up cy-panzoom-pan-button"></div>');
          var $pDown = $('<div class="cy-panzoom-pan-down cy-panzoom-pan-button"></div>');
          var $pLeft = $('<div class="cy-panzoom-pan-left cy-panzoom-pan-button"></div>');
          var $pRight = $('<div class="cy-panzoom-pan-right cy-panzoom-pan-button"></div>');
          $panner.append( $pUp ).append( $pDown ).append( $pLeft ).append( $pRight );

          var $pIndicator = $('<div class="cy-panzoom-pan-indicator"></div>');
          $panner.append( $pIndicator );

          // functions for calculating panning
          ////////////////////////////////////

          function handle2pan(e){
            var v = {
              x: e.originalEvent.pageX - $panner.offset().left - $panner.width()/2,
              y: e.originalEvent.pageY - $panner.offset().top - $panner.height()/2
            }

            var r = options.panDragAreaSize;
            var d = Math.sqrt( v.x*v.x + v.y*v.y );
            var percent = Math.min( d/r, 1 );

            if( d < options.panInactiveArea ){
              return {
                x: NaN,
                y: NaN
              };
            }

            v = {
              x: v.x/d,
              y: v.y/d
            };

            percent = Math.max( options.panMinPercentSpeed, percent );

            var vnorm = {
              x: -1 * v.x * (percent * options.panDistance),
              y: -1 * v.y * (percent * options.panDistance)
            };

            return vnorm;
          }

          function donePanning(){
            clearInterval(panInterval);
            windowUnbind("mousemove", handler);

            $pIndicator.hide();
          }

          function positionIndicator(pan){
            var v = pan;
            var d = Math.sqrt( v.x*v.x + v.y*v.y );
            var vnorm = {
              x: -1 * v.x/d,
              y: -1 * v.y/d
            };

            var w = $panner.width();
            var h = $panner.height();
            var percent = d/options.panDistance;
            var opacity = Math.max( options.panIndicatorMinOpacity, percent );
            var color = 255 - Math.round( opacity * 255 );

            $pIndicator.show().css({
              left: w/2 * vnorm.x + w/2,
              top: h/2 * vnorm.y + h/2,
              background: "rgb(" + color + ", " + color + ", " + color + ")"
            });
          }

          function calculateZoomCenterPoint(){
            var cy = $container.cytoscape("get");
            var pan = cy.pan();
            var zoom = cy.zoom();

            zx = $container.width()/2;
            zy = $container.height()/2;
          }

          var zooming = false;
          function startZooming(){
            zooming = true;

            calculateZoomCenterPoint();
          }


          function endZooming(){
            zooming = false;
          }

          var zx, zy;
          function zoomTo(level){
            var cy = $container.cytoscape("get");

            if( !zooming ){ // for non-continuous zooming (e.g. click slider at pt)
              calculateZoomCenterPoint();
            }

            cy.zoom({
              level: level,
              renderedPosition: { x: zx, y: zy }
            });
          }

          var panInterval;

          var handler = function(e){
            e.stopPropagation(); // don't trigger dragging of panzoom
            e.preventDefault(); // don't cause text selection
            clearInterval(panInterval);

            var pan = handle2pan(e);

            if( isNaN(pan.x) || isNaN(pan.y) ){
              $pIndicator.hide();
              return;
            }

            positionIndicator(pan);
            panInterval = setInterval(function(){
              $container.cytoscape("get").panBy(pan);
            }, options.panSpeed);
          };

          $pHandle.bind("mousedown", function(e){
            // handle click of icon
            handler(e);

            // update on mousemove
            windowBind("mousemove", handler);
          });

          $pHandle.bind("mouseup", function(){
            donePanning();
          });

          windowBind("mouseup blur", function(){
            donePanning();
          });



          // set up slider behaviour
          //////////////////////////

          $slider.bind('mousedown', function(){
            return false; // so we don't pan close to the slider handle
          });

          var sliderVal;
          var sliding = false;
          var sliderPadding = 2;

          function setSliderFromMouse(evt, handleOffset){
            if( handleOffset === undefined ){
              handleOffset = 0;
            }

            var padding = sliderPadding;
            var min = 0 + padding;
            var max = $slider.height() - $sliderHandle.height() - 2*padding;
            var top = evt.pageY - $slider.offset().top - handleOffset;

            // constrain to slider bounds
            if( top < min ){ top = min }
            if( top > max ){ top = max }

            var percent = 1 - (top - min) / ( max - min );

            // move the handle
            $sliderHandle.css('top', top);

            var zmin = options.minZoom;
            var zmax = options.maxZoom;

            // assume (zoom = zmax ^ p) where p ranges on (x, 1) with x negative
            var x = Math.log(zmin) / Math.log(zmax);
            var p = (1 - x)*percent + x;

            // change the zoom level
            var z = Math.pow( zmax, p );

            // bound the zoom value in case of floating pt rounding error
            if( z < zmin ){
              z = zmin;
            } else if( z > zmax ){
              z = zmax;
            }

            zoomTo( z );
          }

          var sliderMdownHandler, sliderMmoveHandler;
          $sliderHandle.bind('mousedown', sliderMdownHandler = function( mdEvt ){
            var handleOffset = mdEvt.target === $sliderHandle[0] ? mdEvt.offsetY : 0;
            sliding = true;

            startZooming();
            $sliderHandle.addClass("active");

            var lastMove = 0;
            windowBind('mousemove', sliderMmoveHandler = function( mmEvt ){
              var now = +new Date;

              // throttle the zooms every 10 ms so we don't call zoom too often and cause lag
              if( now > lastMove + 10 ){
                lastMove = now;
              } else {
                return false;
              }

              setSliderFromMouse(mmEvt, handleOffset);

              return false;
            });

            // unbind when
            windowBind('mouseup', function(){
              windowUnbind('mousemove', sliderMmoveHandler);
              sliding = false;

              $sliderHandle.removeClass("active");
              endZooming();
            });

            return false;
          });

          $slider.bind('mousedown', function(e){
            if( e.target !== $sliderHandle[0] ){
              sliderMdownHandler(e);
              setSliderFromMouse(e);
            }
          });

          function positionSliderFromZoom(){
            var cy = $container.cytoscape("get");
            var z = cy.zoom();
            var zmin = options.minZoom;
            var zmax = options.maxZoom;

            // assume (zoom = zmax ^ p) where p ranges on (x, 1) with x negative
            var x = Math.log(zmin) / Math.log(zmax);
            var p = Math.log(z) / Math.log(zmax);
            var percent = 1 - (p - x) / (1 - x); // the 1- bit at the front b/c up is in the -ve y direction

            var min = sliderPadding;
            var max = $slider.height() - $sliderHandle.height() - 2*sliderPadding;
            var top = percent * ( max - min );

            // constrain to slider bounds
            if( top < min ){ top = min }
            if( top > max ){ top = max }

            // move the handle
            $sliderHandle.css('top', top);
          }

          positionSliderFromZoom();

          cyOn('zoom', function(){
            if( !sliding ){
              positionSliderFromZoom();
            }
          });

          // set the position of the zoom=1 tick
          (function(){
            var z = 1;
            var zmin = options.minZoom;
            var zmax = options.maxZoom;

            // assume (zoom = zmax ^ p) where p ranges on (x, 1) with x negative
            var x = Math.log(zmin) / Math.log(zmax);
            var p = Math.log(z) / Math.log(zmax);
            var percent = 1 - (p - x) / (1 - x); // the 1- bit at the front b/c up is in the -ve y direction

            if( percent > 1 || percent < 0 ){
              $noZoomTick.hide();
              return;
            }

            var min = sliderPadding;
            var max = $slider.height() - $sliderHandle.height() - 2*sliderPadding;
            var top = percent * ( max - min );

            // constrain to slider bounds
            if( top < min ){ top = min }
            if( top > max ){ top = max }

            $noZoomTick.css('top', top);
          })();

          // set up zoom in/out buttons
          /////////////////////////////

          function bindButton($button, factor){
            var zoomInterval;

            $button.bind("mousedown", function(e){
              e.preventDefault();
              e.stopPropagation();

              if( e.button != 0 ){
                return;
              }

              var cy = $container.cytoscape("get");
              var doZoom = function(){
                var zoom = cy.zoom();
                var lvl = cy.zoom() * factor;

                if( lvl < options.minZoom ){
                  lvl = options.minZoom;
                }

                if( lvl > options.maxZoom ){
                  lvl = options.maxZoom;
                }

                if( (lvl == options.maxZoom && zoom == options.maxZoom) ||
                  (lvl == options.minZoom && zoom == options.minZoom)
                ){
                  return;
                }

                zoomTo(lvl);
              };

              startZooming();
              doZoom();
              zoomInterval = setInterval(doZoom, options.zoomDelay);

              return false;
            });

            windowBind("mouseup blur", function(){
              clearInterval(zoomInterval);
              endZooming();
            });
          }

          bindButton( $zoomIn, (1 + options.zoomFactor) );
          bindButton( $zoomOut, (1 - options.zoomFactor) );

          $reset.bind("mousedown", function(e){
            if( e.button != 0 ){
              return;
            }

            var cy = $container.cytoscape("get");

            if( cy.elements().size() === 0 ){
              cy.reset();
            } else {
              cy.fit( options.fitPadding );
            }

            return false;
          });



        });
      }
    };

    if( functions[fn] ){
      return functions[fn].apply(this, Array.prototype.slice.call( arguments, 1 ));
    } else if( typeof fn == 'object' || !fn ) {
      return functions.init.apply( this, arguments );
    } else {
      $.error("No such function `"+ fn +"` for jquery.cytoscapePanzoom");
    }

    return $(this);
  };


  if( typeof module !== 'undefined' && module.exports ){ // expose as a commonjs module
    module.exports = register;
  }

  if( typeof define !== 'undefined' && define.amd ){ // expose as an amd/requirejs module
    define('cytoscape-panzoom', function(){
      return register;
    });
  }

  if( typeof cytoscape !== 'undefined' ){ // expose to global cytoscape (i.e. window.cytoscape)
    register( cytoscape, jQuery || {} );
  }

})();
