from django.contrib import admin

from .models import SlipMessage


@admin.register(SlipMessage)
class SlipMessageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'get_wallet_name', 'date_vencit',
        'send_due', 'delinquent_due', 'get_slip_id',
        'content'
    )
    search_fields = ('content',)
    list_filter = ('send_due', 'delinquent_due', 'created_at')
    ordering = ('-created_at',)

    def get_slip_id(self, obj):
        return obj.slip.id
    get_slip_id.short_description = 'Boleto ID'

    def get_wallet_name(self, obj):
        return obj.slip.wallet.name
    get_wallet_name.short_description = 'Carteira Name'

    def get_search_results(self, request, queryset, search_term):
        search_term_upper = search_term.strip().upper()

        delinquent_due_term = None
        wallet_term = None

        search_terms = search_term_upper.split(',')

        for term in search_terms:
            if term == 'YE' or term == 'NO':
                delinquent_due_term = term

            else:
                wallet_term = term

        if delinquent_due_term:
            queryset = queryset.filter(delinquent_due=delinquent_due_term)
        if wallet_term:
            queryset = queryset.filter(slip__wallet__name__icontains=wallet_term)

        queryset = queryset.distinct()

        return queryset, False
