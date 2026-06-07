import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import random
import string

load_dotenv()
TOKEN = os.environ.get("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

BRAND = "Fast Brawl Services"

PAYMENT_DETAILS = {
    "PayPal": "📧 **PayPal:** dahn3854@gmail.com",
    "Revolut": "💳 **Revolut:** @dongnnb0b",
    "Apple Pay": "🔗 **Apple Pay:** https://revolut.me/dongnnb0b",
    "Debit/Credit Card": "🔗 **Debit/Credit Card:** https://revolut.me/dongnnb0b",
    "Bank Transfer": "👤 A staff member will provide bank transfer details shortly.",
    "PayPal Gift Card": "👤 A staff member will provide PayPal Gift Card details shortly.",
    "Crypto": "👤 A staff member will provide crypto details shortly.",
    "PaySafe Card": "👤 A staff member will provide PaySafe details shortly.",
}

SERVICE_ACTIVE_CHANNELS = {
    "ranked": "🟢｜active-ranked",
    "bulk-trophies": "🟢｜active-bulk-trophies",
    "prestige": "🟢｜active-prestige",
    "matcherino": "🟢｜active-matcherino",
    "championship": "🟢｜active-championship",
    "winstreaks": "🟢｜active-winstreaks",
    "tier-1": "🟢｜active-tier-1",
    "tier-2": "🟢｜active-tier-2",
    "tier-3": "🟢｜active-tier-3",
}

SERVICE_TITLES = {
    "ranked": ("🏅 Ranked Boost Order", "Your Ranked Boost Order"),
    "bulk-trophies": ("🏆 Trophy Boost Order", "Your Trophy Boost Order"),
    "prestige": ("⭐ Prestige Boost Order", "Your Prestige Boost Order"),
    "matcherino": ("🎯 Matcherino Boost Order", "Your Matcherino Boost Order"),
    "championship": ("🏆 Championship Boost Order", "Your Championship Boost Order"),
    "winstreaks": ("🔥 Winstreak Boost Order", "Your Winstreak Boost Order"),
    "tier-1": ("🥇 Tier 1 Account Order", "Your Tier 1 Account Order"),
    "tier-2": ("🥈 Tier 2 Account Order", "Your Tier 2 Account Order"),
    "tier-3": ("🥉 Tier 3 Account Order", "Your Tier 3 Account Order"),
}

RANKS_CURRENT = [
    "Bronze I", "Bronze II", "Bronze III",
    "Silver I", "Silver II", "Silver III",
    "Gold I", "Gold II", "Gold III",
    "Diamond I", "Diamond II", "Diamond III",
    "Mythic I", "Mythic II", "Mythic III",
    "Legendary I", "Legendary II", "Legendary III",
    "Masters I", "Masters II", "Masters III"
]

RANKS_DESIRED = [
    "Diamond I", "Diamond II", "Diamond III",
    "Mythic I", "Mythic II", "Mythic III",
    "Legendary I", "Legendary II", "Legendary III",
    "Masters I", "Masters II", "Masters III", "Pro"
]

TROPHY_RANGES = [
    "0-10k", "10-20k", "20-30k", "30-40k", "40-50k", "50-60k",
    "60-70k", "70-80k", "80-90k", "90-100k", "100-125k", "125-150k"
]

POWER11 = [
    "0-10", "11-20", "21-30", "31-40", "41-50",
    "51-60", "61-70", "71-80", "81-90", "91-100", "100+"
]

PRESTIGE_CURRENT = ["0 Trophies", "Prestige 1", "Prestige 2", "Prestige 3"]
PRESTIGE_DESIRED = ["Prestige 1", "Prestige 2", "Prestige 3"]
WINSTREAK_OPTIONS = ["50 wins", "67 wins", "69 wins", "101 wins", "111 wins", "125 wins", "200 wins"]
BRAWLER_PICKER = ["Booster chooses (Normal Price)", "I choose the brawler (+€5)"]
MATCHERINO_BRAWLERS = ["60-70 Brawlers", "70-80 Brawlers", "80-90 Brawlers", "90+ Brawlers"]
PAYMENT_OPTIONS = ["PayPal", "Revolut", "Apple Pay", "Bank Transfer", "PayPal Gift Card", "Debit/Credit Card", "Crypto", "PaySafe Card", "Other"]
BUFFIES = ["1-5", "6-10", "11-15", "16-20", "21-25", "26-30", "30+"]
MASTERS_HIGH = ["Masters II", "Masters III", "Pro"]

IMAGES = {
    "ranked": "https://media.discordapp.net/attachments/1512925620169084968/1512959670476865676/image.png?ex=6a25fcfe&is=6a24ab7e&hm=cd95ede6d8e53bd66286ae88b27c7ff850a291308fcb653ed13e189472210812&=&format=webp&quality=lossless&width=2280&height=1272",
    "prestige": "https://media.discordapp.net/attachments/1512925620169084968/1512965912385421352/image.png?ex=6a2602cf&is=6a24b14f&hm=f45e7d5a1059d5ed59791c4417d4d1441614cd7b235f547a239393291175bc0d&=&format=webp&quality=lossless&width=2448&height=1272",
    "bulk-trophies": "https://media.discordapp.net/attachments/1512925620169084968/1512966361150787735/image.png?ex=6a26033a&is=6a24b1ba&hm=727d9d165fa4fdd10fa5653009e2914a9bf06f99b7b5c234710cc225c72d3f05&=&format=webp&quality=lossless&width=1100&height=616",
    "matcherino": "https://media.discordapp.net/attachments/1512925620169084968/1512966584631820490/image.png?ex=6a26036f&is=6a24b1ef&hm=a80906a8a34f53d2418f21b957e7d65d75151b8d18c6b532e5cf951b5652308a&=&format=webp&quality=lossless&width=2262&height=1272",
    "winstreaks": "https://media.discordapp.net/attachments/1512925620169084968/1512967580766175293/image.png?ex=6a26045c&is=6a24b2dc&hm=ee0854a41be7bf0d7314297e4ed9481de2d886daf4a7a8eea56bde763d87f3c4&=&format=webp&quality=lossless&width=1054&height=700",
    "championship": "https://media.discordapp.net/attachments/1512925620169084968/1512967994685526126/image.png?ex=6a2604bf&is=6a24b33f&hm=8c31044313dda43ca7848048e4e063756d3ea8385a65c69d3ea562770fe485dd&=&format=webp&quality=lossless&width=1100&height=438",
}

def generate_ticket_number():
    return ''.join(random.choices(string.digits, k=4))

def get_payment_info(method):
    return PAYMENT_DETAILS.get(method, f"💳 **{method}** — A staff member will confirm details shortly.")

def stars(rating):
    return "⭐" * rating + "☆" * (5 - rating)

def make_options(lst):
    return [discord.SelectOption(label=x, value=x) for x in lst]

# ─────────────────────────────────────────────
# CREATE TICKET
# ─────────────────────────────────────────────
async def create_ticket(guild, service, user, data):
    active_channel_name = SERVICE_ACTIVE_CHANNELS.get(service, "active-ranked")
    active_channel = discord.utils.get(guild.channels, name=active_channel_name)
    if not active_channel:
        return None

    ticket_num = generate_ticket_number()
    thread = await active_channel.create_thread(
        name=f"{user.name}.{ticket_num}",
        type=discord.ChannelType.public_thread,
        auto_archive_duration=10080
    )

    ticket_label, order_title = SERVICE_TITLES.get(service, ("📋 Order Ticket", "Your Order"))

    # Embed 1 — header
    header_embed = discord.Embed(
        title=f"{ticket_label} is now open! 🎮",
        description="**Click the button below to close this ticket when you're done.**",
        color=discord.Color.green()
    )
    header_embed.set_footer(text=f"Powered by {BRAND}")

    # Embed 2 — order details
    details_embed = discord.Embed(
        title=f"ℹ️ Order Details",
        description=f"**{order_title}**",
        color=discord.Color.purple()
    )

    for key, value in data.items():
        if key == "Notes" and value == "None":
            continue
        details_embed.add_field(name=key, value=f"╰ {value}", inline=False)

    details_embed.add_field(name="Customer", value=f"╰ {user.mention}", inline=False)

    payment_method = data.get("Payment Method", "")
    details_embed.add_field(name="💳 Payment Details", value=get_payment_info(payment_method), inline=False)
    details_embed.set_footer(text=f"Powered by {BRAND} • Ticket #{ticket_num}")

    await thread.send(embeds=[header_embed, details_embed], view=CloseTicketView())
    await thread.add_user(user)

    # Ping owner
    owner_role = discord.utils.get(guild.roles, name="Owner")
    if owner_role:
        await thread.send(f"{owner_role.mention} New ticket opened!", delete_after=5)

    return thread

# ─────────────────────────────────────────────
# CLOSE TICKET
# ─────────────────────────────────────────────
class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Ticket closed.", ephemeral=True)
        if isinstance(interaction.channel, discord.Thread):
            await interaction.channel.edit(archived=True, locked=True)

    @discord.ui.button(label="Close With Reason", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket_reason")
    async def close_with_reason(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CloseReasonModal())

class CloseReasonModal(discord.ui.Modal, title="Close Ticket With Reason"):
    reason = discord.ui.TextInput(label="Reason", placeholder="Enter reason...", max_length=500)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Closed: {self.reason.value}", ephemeral=True)
        if isinstance(interaction.channel, discord.Thread):
            await interaction.channel.edit(archived=True, locked=True)

# ─────────────────────────────────────────────
# CONFIRM VIEW (Fixed)
# ─────────────────────────────────────────────
class ConfirmOrderView(discord.ui.View):
    def __init__(self, service, data):
        super().__init__(timeout=None)
        self.service = service
        self.data = data

    @discord.ui.button(label="✅ Confirm & Create Ticket", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        thread = await create_ticket(interaction.guild, self.service, interaction.user, self.data)
        if thread:
            await interaction.response.edit_message(content=f"✅ Ticket created: {thread.mention}\nA staff member will confirm your price shortly.", embed=None, view=None)
        else:
            await interaction.response.edit_message(content="❌ Could not find active channel. Contact an admin.", embed=None, view=None)

    @discord.ui.button(label="🔄 Change Selections", style=discord.ButtonStyle.secondary)
    async def change(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Please click Order Now again to restart.", embed=None, view=None)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="❌ Order cancelled.", embed=None, view=None)

def build_confirm_embed(service_name, data):
    embed = discord.Embed(
        title=f"🎯 Confirm Your {service_name} Order",
        description="**Please review your order details and confirm:**",
        color=discord.Color.purple()
    )
    for key, value in data.items():
        if key == "Notes" and value == "None":
            continue
        embed.add_field(name=key, value=f"> {value}", inline=False)

    embed.set_footer(text=f"Powered by {BRAND} | Account info is hidden for security")
    return embed

# ─────────────────────────────────────────────
# ADDITIONAL NOTES MODAL
# ─────────────────────────────────────────────
class AdditionalNotesModal(discord.ui.Modal, title="Additional Notes (Optional)"):
    notes = discord.ui.TextInput(label="Notes", placeholder="Any special requests...", required=False, max_length=500, style=discord.TextStyle.paragraph)

    def __init__(self, service, service_name, data):
        super().__init__()
        self.service = service
        self.service_name = service_name
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        self.data["Notes"] = self.notes.value if self.notes.value else "None"
        embed = build_confirm_embed(self.service_name, self.data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView(self.service, self.data), ephemeral=True)

# ─────────────────────────────────────────────
# OTHER PAYMENT & NOTES MODAL (Fixed)
# ─────────────────────────────────────────────
class OtherPaymentAndNotesModal(discord.ui.Modal, title="Payment & Notes"):
    payment = discord.ui.TextInput(label="Payment Method", placeholder="Enter your payment method...", max_length=50)
    notes = discord.ui.TextInput(label="Notes (Optional)", placeholder="Any special requests...", required=False, max_length=500, style=discord.TextStyle.paragraph)

    def __init__(self, service, service_name, data):
        super().__init__()
        self.service = service
        self.service_name = service_name
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        self.data["Payment Method"] = self.payment.value
        self.data["Notes"] = self.notes.value if self.notes.value else "None"
        embed = build_confirm_embed(self.service_name, self.data)
        await interaction.response.send_message(embed=embed, view=ConfirmOrderView(self.service, self.data), ephemeral=True)

# ─────────────────────────────────────────────
# PAYMENT VIEW (reusable)
# ─────────────────────────────────────────────
class PaymentView(discord.ui.View):
    def __init__(self, service, service_name, data, custom_id_suffix):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

        select = discord.ui.Select(
            placeholder="Select payment method...",
            custom_id=f"payment_{custom_id_suffix}",
            options=make_options(PAYMENT_OPTIONS)
        )
        select.callback = self.on_select
        self.add_item(select)

    def get_prompt(self):
        return "**Select your payment method:**"

    async def on_select(self, interaction: discord.Interaction):
        value = interaction.data["values"][0]
        if value == "Other":
            await interaction.response.send_modal(OtherPaymentAndNotesModal(self.service, self.service_name, self.data))
        else:
            self.data["Payment Method"] = value
            await interaction.response.send_modal(AdditionalNotesModal(self.service, self.service_name, self.data))

# ─────────────────────────────────────────────
# RANKED FLOW
# ─────────────────────────────────────────────
class RankedCurrentRankView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**Select your current rank:**"

    @discord.ui.select(placeholder="Select current rank...", custom_id="ranked_current", options=make_options(RANKS_CURRENT))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Current Rank"] = select.values[0]
        view = RankedDesiredRankView(self.service, self.service_name, self.data)
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class RankedDesiredRankView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**Select your desired rank:**"

    @discord.ui.select(placeholder="Select desired rank...", custom_id="ranked_desired", options=make_options(RANKS_DESIRED))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Desired Rank"] = select.values[0]
        if select.values[0] in MASTERS_HIGH:
            view = RankedBuffiesView(self.service, self.service_name, self.data)
            await interaction.response.edit_message(content=view.get_prompt(), view=view)
        else:
            view = RankedPower11View(self.service, self.service_name, self.data)
            await interaction.response.edit_message(content=view.get_prompt(), view=view)

class RankedBuffiesView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**How many buffies do you have unlocked?**"

    @discord.ui.select(placeholder="Select buffies...", custom_id="ranked_buffies", options=make_options(BUFFIES))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Buffies Unlocked"] = select.values[0]
        view = RankedPower11View(self.service, self.service_name, self.data)
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class RankedPower11View(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**How many Power 11 brawlers do you have?**"

    @discord.ui.select(placeholder="Select Power 11 count...", custom_id="ranked_power11", options=make_options(POWER11))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Power 11 Brawlers"] = select.values[0]
        view = PaymentView(self.service, self.service_name, self.data, "ranked")
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class RankedOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="ranked_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=RankedBoostCarryView(), ephemeral=True)

class RankedBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="ranked_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Boost"}
        view = RankedCurrentRankView("ranked", "Ranked Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="ranked_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Carry"}
        view = RankedCurrentRankView("ranked", "Ranked Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

# ─────────────────────────────────────────────
# TROPHIES FLOW
# ─────────────────────────────────────────────
class TrophiesCurrentView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**Select your current trophy range:**"

    @discord.ui.select(placeholder="Select current trophy range...", custom_id="trophies_current", options=make_options(TROPHY_RANGES))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Current Trophy Range"] = select.values[0]
        view = TrophiesDesiredView(self.service, self.service_name, self.data)
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class TrophiesDesiredView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**Select your desired trophy range:**"

    @discord.ui.select(placeholder="Select desired trophy range...", custom_id="trophies_desired", options=make_options(TROPHY_RANGES))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Desired Trophy Range"] = select.values[0]
        view = TrophiesPower11View(self.service, self.service_name, self.data)
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class TrophiesPower11View(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**How many Power 11 brawlers do you have?**"

    @discord.ui.select(placeholder="Select Power 11 count...", custom_id="trophies_power11", options=make_options(POWER11))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Power 11 Brawlers"] = select.values[0]
        view = PaymentView(self.service, self.service_name, self.data, "trophies")
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class TrophiesOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="trophies_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=TrophiesBoostCarryView(), ephemeral=True)

class TrophiesBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="trophies_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Boost"}
        view = TrophiesCurrentView("bulk-trophies", "Trophy Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="trophies_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Carry"}
        view = TrophiesCurrentView("bulk-trophies", "Trophy Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

# ─────────────────────────────────────────────
# PRESTIGE FLOW
# ─────────────────────────────────────────────
class PrestigeBrawlerModal(discord.ui.Modal, title="Enter Brawler Name"):
    brawler = discord.ui.TextInput(label="Brawler Name", placeholder="Enter brawler name...", max_length=30)

    def __init__(self, service, service_name, data):
        super().__init__()
        self.service = service
        self.service_name = service_name
        self.data = data

    async def on_submit(self, interaction: discord.Interaction):
        self.data["Brawler"] = self.brawler.value
        view = PrestigeCurrentView(self.service, self.service_name, self.data)
        await interaction.response.send_message(content=view.get_prompt(), view=view, ephemeral=True)

class PrestigeCurrentView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**Select your current prestige:**"

    @discord.ui.select(placeholder="Select current prestige...", custom_id="prestige_current", options=make_options(PRESTIGE_CURRENT))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Current Prestige"] = select.values[0]
        view = PrestigeDesiredView(self.service, self.service_name, self.data)
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class PrestigeDesiredView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**Select your desired prestige:**"

    @discord.ui.select(placeholder="Select desired prestige...", custom_id="prestige_desired", options=make_options(PRESTIGE_DESIRED))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Desired Prestige"] = select.values[0]
        view = PaymentView(self.service, self.service_name, self.data, "prestige")
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class PrestigeOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="prestige_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=PrestigeBoostCarryView(), ephemeral=True)

class PrestigeBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="prestige_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Boost"}
        await interaction.response.send_modal(PrestigeBrawlerModal("prestige", "Prestige Boost", data))

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="prestige_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Carry"}
        await interaction.response.send_modal(PrestigeBrawlerModal("prestige", "Prestige Boost", data))

# ─────────────────────────────────────────────
# WINSTREAK FLOW
# ─────────────────────────────────────────────
class WinstreakTargetView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**Select your target winstreak:**"

    @discord.ui.select(placeholder="Select target winstreak...", custom_id="winstreak_target", options=make_options(WINSTREAK_OPTIONS))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Target Winstreak"] = select.values[0]
        view = WinstreakPickerView(self.service, self.service_name, self.data)
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class WinstreakPickerView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**Who chooses the brawler?**"

    @discord.ui.select(placeholder="Select who picks the brawler...", custom_id="winstreak_picker", options=make_options(BRAWLER_PICKER))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Brawler Picker"] = select.values[0]
        view = WinstreakPower11View(self.service, self.service_name, self.data)
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class WinstreakPower11View(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**How many Power 11 brawlers do you have?**"

    @discord.ui.select(placeholder="Select Power 11 count...", custom_id="winstreak_power11", options=make_options(POWER11))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Power 11 Brawlers"] = select.values[0]
        view = PaymentView(self.service, self.service_name, self.data, "winstreak")
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class WinstreakOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="winstreak_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=WinstreakBoostCarryView(), ephemeral=True)

class WinstreakBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="winstreak_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Boost"}
        view = WinstreakTargetView("winstreaks", "Winstreak Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="winstreak_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Carry"}
        view = WinstreakTargetView("winstreaks", "Winstreak Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

# ─────────────────────────────────────────────
# MATCHERINO / CHAMPIONSHIP FLOW
# ─────────────────────────────────────────────
class MatchBrawlerView(discord.ui.View):
    def __init__(self, service, service_name, data):
        super().__init__(timeout=None)
        self.service = service
        self.service_name = service_name
        self.data = data

    def get_prompt(self):
        return "**How many brawlers do you have?**"

    @discord.ui.select(placeholder="Select brawler count...", custom_id="match_brawlers", options=make_options(MATCHERINO_BRAWLERS))
    async def select(self, interaction: discord.Interaction, select: discord.ui.Select):
        self.data["Brawler Count"] = select.values[0]
        view = PaymentView(self.service, self.service_name, self.data, "match")
        await interaction.response.edit_message(content=view.get_prompt(), view=view)

class MatcherinoOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="matcherino_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=MatcherinoBoostCarryView(), ephemeral=True)

class MatcherinoBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="matcherino_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Boost"}
        view = MatchBrawlerView("matcherino", "Matcherino Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="matcherino_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Carry"}
        view = MatchBrawlerView("matcherino", "Matcherino Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

class ChampionshipOrderView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id="championship_order_now")
    async def order_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Choose your service type:", description="🚀 **B00st** - Standard service\n🤝 **Carry** - Play together (2x price)", color=discord.Color.purple())
        await interaction.response.send_message(embed=embed, view=ChampionshipBoostCarryView(), ephemeral=True)

class ChampionshipBoostCarryView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get B00sted", style=discord.ButtonStyle.success, emoji="🚀", custom_id="championship_boost")
    async def boost(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Boost"}
        view = MatchBrawlerView("championship", "Championship Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

    @discord.ui.button(label="Get Carried (2x Price)", style=discord.ButtonStyle.primary, emoji="🤝", custom_id="championship_carry")
    async def carry(self, interaction: discord.Interaction, button: discord.ui.Button):
        data = {"Order Type": "Carry"}
        view = MatchBrawlerView("championship", "Championship Boost", data)
        await interaction.response.edit_message(content=view.get_prompt(), embed=None, view=view)

# ─────────────────────────────────────────────
# TIER FLOW
# ─────────────────────────────────────────────
class TierOrderView(discord.ui.View):
    def __init__(self, tier, service):
        super().__init__(timeout=None)
        self.tier = tier
        self.service = service
        btn = discord.ui.Button(label="Order Now", style=discord.ButtonStyle.success, emoji="⚡", custom_id=f"tier_{tier}_order_now")
        btn.callback = self.order_now
        self.add_item(btn)

    async def order_now(self, interaction: discord.Interaction):
        data = {"Account Tier": f"Tier {self.tier}"}
        view = PaymentView(self.service, f"Tier {self.tier} Account", data, f"tier{self.tier}")
        await interaction.response.send_message(content=view.get_prompt(), view=view, ephemeral=True)

# ─────────────────────────────────────────────
# ORDER-HERE DROPDOWN
# ─────────────────────────────────────────────
class ServiceSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        placeholder="Select a service...",
        custom_id="main_service_select",
        options=[
            discord.SelectOption(label="Boost / Carry Service", description="Trophy, Ranked, Prestige, Winstreak, Matcherino & more", emoji="📊"),
            discord.SelectOption(label="Other Queries", description="General questions, support & other requests", emoji="🎫"),
        ]
    )
    async def select_service(self, interaction: discord.Interaction, select: discord.ui.Select):
        value = select.values[0]
        if value == "Boost / Carry Service":
            guild = interaction.guild
            def ch(name):
                c = discord.utils.get(guild.channels, name=name)
                return c.mention if c else name

            embed = discord.Embed(title="📊 Boost & Carry Services", description="ℹ️ Click the channel that matches your desired service.", color=discord.Color.purple())
            embed.add_field(name="", value=(
                f"> **Trophy** — {ch('⚡｜bulk-trophies')}\n"
                f"> **Matcherino** — {ch('⚡｜matcherino')}\n"
                f"> **Ranked** — {ch('⚡｜ranked')}\n"
                f"> **Winstreak** — {ch('⚡｜winstreaks')}\n"
                f"> **Prestige** — {ch('⚡｜prestige')}\n"
                f"> **Championship** — {ch('⚡｜championship-challenge')}"
            ), inline=False)
            embed.set_footer(text=f"Powered by {BRAND}")
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            guild = interaction.guild
            others_channel = discord.utils.get(guild.channels, name="🟢｜active-support")
            if others_channel:
                thread = await others_channel.create_thread(name=f"Support — {interaction.user.name}", type=discord.ChannelType.public_thread, auto_archive_duration=10080)
                embed = discord.Embed(title="🎫 Support Ticket Opened", description=f"Welcome {interaction.user.mention}! A staff member will be with you shortly.", color=discord.Color.blue())
                embed.set_footer(text=f"Powered by {BRAND}")
                await thread.send(embed=embed, view=CloseTicketView())
                await thread.add_user(interaction.user)

                owner_role = discord.utils.get(guild.roles, name="Owner")
                if owner_role:
                    await thread.send(f"{owner_role.mention} New support ticket!", delete_after=5)

                await interaction.response.send_message(f"✅ Support ticket created: {thread.mention}", ephemeral=True)
            else:
                await interaction.response.send_message("Support channel not found. Contact an admin.", ephemeral=True)

# ────────────────────────────────────────
