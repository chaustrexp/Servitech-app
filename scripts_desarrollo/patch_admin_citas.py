import codecs

# 1. Update HTML
path_html = 'c:/Servitech/Servitech-app/turnos/templates/turnos/administracion/admin_citas.html'
with codecs.open(path_html, 'r', 'utf-8') as f:
    html = f.read()

html = html.replace('\r\n', '\n')

old_acciones = '''                    <!-- Acciones -->
                    <td class="py-4 px-6 text-right col-acciones">
                        <a href="{% url 'detalle_cita' cita.id %}" class="p-1.5 rounded-lg text-slate-400 hover:bg-slate-100 hover:text-slate-600 transition inline-block" title="Ver detalles">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                            </svg>
                        </a>
                    </td>'''

new_acciones = '''                    <!-- Acciones -->
                    <td class="py-4 px-6 text-right col-acciones">
                        <div class="flex items-center justify-end gap-1">
                            <a href="{% url 'detalle_cita' cita.id %}" class="p-1.5 rounded-lg text-slate-400 hover:bg-blue-50 hover:text-blue-600 transition inline-block" title="Ver detalles">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                                </svg>
                            </a>
                            
                            <form method="POST" action="{% url 'admin_citas' %}" class="inline-block" onsubmit="return confirm('¿Marcar como cancelada esta cita?');">
                                {% csrf_token %}
                                <input type="hidden" name="accion" value="cancelar_cita">
                                <input type="hidden" name="cita_id" value="{{ cita.id }}">
                                <button type="submit" class="p-1.5 rounded-lg text-slate-400 hover:bg-rose-50 hover:text-rose-600 transition" title="Cancelar cita">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                </button>
                            </form>
                            
                            <form method="POST" action="{% url 'admin_citas' %}" class="inline-block" onsubmit="return confirm('¿Eliminar permanentemente esta cita del registro?');">
                                {% csrf_token %}
                                <input type="hidden" name="accion" value="eliminar_cita">
                                <input type="hidden" name="cita_id" value="{{ cita.id }}">
                                <button type="submit" class="p-1.5 rounded-lg text-slate-400 hover:bg-red-100 hover:text-red-600 transition" title="Eliminar definitivamente">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                </button>
                            </form>
                        </div>
                    </td>'''

if old_acciones in html:
    html = html.replace(old_acciones, new_acciones)
    with codecs.open(path_html, 'w', 'utf-8') as f:
        f.write(html)
    print('HTML updated!')
else:
    print('WARNING: Old acciones block not found in HTML!')


# 2. Update views
path_views = 'c:/Servitech/Servitech-app/turnos/views/dashboard_views.py'
with codecs.open(path_views, 'r', 'utf-8') as f:
    views = f.read()

views = views.replace('\r\n', '\n')

old_views = '''def admin_citas(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')

    hoy = date.today()'''

new_views = '''def admin_citas(request):
    if request.user.rol != Usuario.Rol.ADMINISTRADOR:
        return redirect('home')
        
    if request.method == 'POST':
        accion = request.POST.get('accion')
        cita_id = request.POST.get('cita_id')
        if accion == 'cancelar_cita' and cita_id:
            from turnos.models import Cita, EstadoCita
            try:
                cita = Cita.objects.get(id=cita_id)
                estado_cancelada, _ = EstadoCita.objects.get_or_create(nombre='Cancelada')
                cita.estado = estado_cancelada
                cita.save()
                messages.success(request, f'La cita #{cita.id} ha sido marcada como cancelada.')
            except Cita.DoesNotExist:
                messages.error(request, 'Cita no encontrada.')
        elif accion == 'eliminar_cita' and cita_id:
            from turnos.models import Cita
            try:
                cita = Cita.objects.get(id=cita_id)
                cita_id_num = cita.id
                cita.delete()
                messages.success(request, f'La cita #{cita_id_num} ha sido eliminada definitivamente.')
            except Cita.DoesNotExist:
                messages.error(request, 'Cita no encontrada.')
        return redirect('admin_citas')

    hoy = date.today()'''

if old_views in views:
    views = views.replace(old_views, new_views)
    with codecs.open(path_views, 'w', 'utf-8') as f:
        f.write(views)
    print('Views updated!')
else:
    print('WARNING: Old views block not found!')

