<template>
  <div class="min-h-screen bg-gray-50 py-12 px-6">
    <div class="max-w-3xl mx-auto bg-white border border-gray-200 rounded-2xl p-10">

      <header class="text-center mb-10">
        <h1 class="text-2xl font-bold text-gray-800 tracking-tight">Aviso Legal y Condiciones Generales de Uso</h1>
        <p class="text-sm text-gray-400 mt-1">makemenu.arkania.es</p>
      </header>

      <div class="prose prose-sm max-w-none text-gray-600 space-y-6">

        <section>
          <h2 class="text-lg font-bold text-gray-800 mb-2">I. Información general</h2>
          <p>En cumplimiento con el deber de información dispuesto en la Ley 34/2002 de Servicios de la Sociedad de la Información y el Comercio Electrónico (LSSI-CE) de 11 de julio, se facilitan a continuación los siguientes datos de información general de este sitio web:</p>
          <p class="mt-2">La titularidad de este sitio web, makemenu.arkania.es, la ostenta: <strong>MakeMenu S.L</strong>, provista de NIF: A58447470 e inscrita en: Registro Mercantil Santa Cruz de Tenerife, cuyo representante es: Cristian Reyes Hernández, Samuel Domingo Cruz Sánchez, Daniele Dettori.</p>
          <p class="mt-1">Dirección: Avenida Melchor Luz</p>
          <p>Teléfono de contacto: 650935014</p>
          <p>Email de contacto: makemenu@gmail.com</p>
        </section>

        <section>
          <h2 class="text-lg font-bold text-gray-800 mb-2">II. Términos y condiciones generales de uso</h2>

          <h3 class="text-base font-semibold text-gray-700 mt-4 mb-2">El objeto de las condiciones: El Sitio Web</h3>
          <p>El objeto de las presentes Condiciones Generales de Uso es regular el acceso y la utilización del Sitio Web. MakeMenu se reserva la facultad de modificar, en cualquier momento, y sin aviso previo, la presentación y configuración del Sitio Web y de los Contenidos y Servicios en él incorporados.</p>
          <p class="mt-2">Algunos de los Contenidos o Servicios ofrecidos por MakeMenu a través del Sitio Web pueden encontrarse sujetos a la contratación previa del Contenido o Servicio. La utilización de alguno de los Contenidos o Servicios del Sitio Web podrá hacerse mediante la suscripción o registro previo del Usuario.</p>

          <h3 class="text-base font-semibold text-gray-700 mt-4 mb-2">El Usuario</h3>
          <p>El acceso, la navegación y uso del Sitio Web confiere la condición de Usuario, por lo que se aceptan, desde que se inicia la navegación por el Sitio Web, todas las Condiciones aquí establecidas. El Sitio Web de MakeMenu proporciona gran diversidad de información, servicios y datos. El Usuario asume su responsabilidad para realizar un uso correcto del Sitio Web.</p>
          <ul class="list-disc pl-5 space-y-1 mt-2">
            <li>Un uso de la información, Contenidos y/o Servicios sin que sea contrario a lo dispuesto por las presentes Condiciones, la Ley, la moral o el orden público.</li>
            <li>La veracidad y licitud de las informaciones aportadas por el Usuario en los formularios extendidos por MakeMenu.</li>
          </ul>
          <p class="mt-2">El Usuario declara ser mayor de edad y disponer de la capacidad jurídica suficiente para vincularse por las presentes Condiciones. El Sitio Web está dirigido principalmente a Usuarios residentes en España.</p>
        </section>

        <section>
          <h2 class="text-lg font-bold text-gray-800 mb-2">III. Acceso y navegación: exclusión de garantías y responsabilidad</h2>
          <p>MakeMenu no garantiza la continuidad, disponibilidad y utilidad del Sitio Web, ni de los Contenidos o Servicios. MakeMenu hará todo lo posible por el buen funcionamiento del Sitio Web, sin embargo, no se responsabiliza ni garantiza que el acceso a este Sitio Web no vaya a ser ininterrumpido o que esté libre de error.</p>
          <p class="mt-2">En ningún caso MakeMenu será responsable por las pérdidas, daños o perjuicios de cualquier tipo que surjan por el acceso, navegación y el uso del Sitio Web.</p>
        </section>

        <section>
          <h2 class="text-lg font-bold text-gray-800 mb-2">IV. Política de enlaces</h2>
          <p>El Sitio Web de MakeMenu pone o puede poner a disposición de los Usuarios medios de enlace que permiten acceder a sitios web pertenecientes y/o gestionados por terceros. MakeMenu no asume ninguna responsabilidad por los daños y perjuicios que pudieran producirse por el acceso o uso de los contenidos de los sitios web no gestionados por MakeMenu.</p>
          <p class="mt-2">No se permite la reproducción —total o parcialmente— de ninguno de los Contenidos y/o Servicios del Sitio Web sin autorización expresa de MakeMenu.</p>
        </section>

        <section>
          <h2 class="text-lg font-bold text-gray-800 mb-2">V. Propiedad intelectual e industrial</h2>
          <p>MakeMenu por sí o como parte cesionaria, es titular de todos los derechos de propiedad intelectual e industrial del Sitio Web, así como de los elementos contenidos en el mismo. Todos los derechos reservados.</p>
          <p class="mt-2">El Usuario se compromete a respetar los derechos de propiedad intelectual e industrial de MakeMenu. Podrá visualizar los elementos del Sitio Web o incluso imprimirlos, copiarlos y almacenarlos exclusivamente para su uso personal.</p>
        </section>

        <section>
          <h2 class="text-lg font-bold text-gray-800 mb-2">VI. Acciones legales, legislación aplicable y jurisdicción</h2>
          <p>MakeMenu se reserva la facultad de presentar las acciones civiles o penales que considere necesarias por la utilización indebida del Sitio Web y Contenidos, o por el incumplimiento de las presentes Condiciones.</p>
          <p class="mt-2">La relación entre el Usuario y MakeMenu se regirá por la normativa vigente y de aplicación en el territorio español.</p>
        </section>

      </div>

      <div class="mt-10 pt-6 border-t border-gray-100 text-center">
        <RouterLink :to="{ name: 'home' }" class="text-sm text-emerald-600 hover:text-emerald-700 font-medium">
          ← Volver al inicio
        </RouterLink>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>