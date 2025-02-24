
def phone_format(phone: str):
    # return re.sub(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', phone)
    if not phone.isdigit() or len(phone) != 10:
        return ''
    return f"{phone[:3]}-{phone[3:6]}-{phone[6:]}"
