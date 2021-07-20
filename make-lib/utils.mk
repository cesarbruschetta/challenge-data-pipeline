define check-var
ifndef $(1)
$$(error <$(1)> is a required variable!)
endif
endef
